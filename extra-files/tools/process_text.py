"""Text processing"""
import re
import shutil


def mlength(iterable) -> int:
    """Get the length of the longest element in the sequence"""

    lengths = []
    for item in iterable:
        if isinstance(item, (list, tuple)):
            mitem = mlength(item)
            lengths.append(mitem)
        else:
            lengths.append(len(str(item)))

    try:
        return max(lengths)
    except ValueError:
        return 0


def rectangles(*iterables) -> tuple[list, list]:
    """Get the length (number of elements) and 
    width (length of the longest element) of multiple sequences
    """

    lengths = []
    widths = []
    for col in iterables:
        lengths.append(len(col))
        widths.append(mlength(col))
    return lengths, widths


def to_markdown_table(*iterables) -> str:
    """Convert multiple sequences to Markdown tables"""

    # Calculate the maximum width of each column and
    # check if all columns have the same number of elements
    col_lengths, col_widths = rectangles(*iterables)
    if len(set(col_lengths)) != 1:
        print('The number of elements in multiple columns is not equal,'
              'and they cannot be matched one-to-one')
        return ''

    # Create table header
    header = '|' + '|'.join(str(lst[0]).center(col_widths[i])
                            for i, lst in enumerate(iterables)) + '|\n'
    separator = '|' + \
                '|'.join('-' * (col_widths[i]) for i in range(len(iterables))) + '|\n'

    # Create table content
    rows = ''
    for i in range(1, col_lengths[0]):
        row = '|'
        for j, lst in enumerate(iterables):
            if i < len(lst):
                if isinstance(lst[i], (list, tuple)):
                    row += '<br>'.join(map(str, lst[i])).center(col_widths[j])
                else:
                    row += str(lst[i]).center(col_widths[j])
            row += '|'
        row += '\n'
        rows += row

    # Return the complete Markdown table
    return header + separator + rows


def manifest_to_lists(file) -> tuple[list, list]:
    """Convert manifest file into two lists"""

    with open(file, encoding='utf-8') as f:
        text = f.read()
    p1 = re.compile(r'^(kernel.*).{25}$', re.MULTILINE)
    p2 = re.compile(r'^(?!.*lib\S|ruby-|.*mod-|.*i18n)(.*) - (.*)', re.MULTILINE)
    text = p1.sub(r'\1', text)
    m = p2.findall(text)
    package, version = zip(*m)
    return list(package), list(version)


def check_header_existence(config):
    with open(config, encoding='utf-8') as f:
        for line in f:
            if line.startswith('CONFIG_TARGET'):
                return True
            if 'CONFIG_PACKAGE' in line:
                return False
    return False


def generate_header(headers: dict, model: str) -> str:
    t1, t2, t3 = headers[model][1:4]
    header = (
        '# Target\n'
        f'CONFIG_TARGET_{t1}=y\n'
        f'CONFIG_TARGET_{t1}_{t2}=y\n'
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{t3}=y\n')
    return header


def modify_config_header(config, header, new_file=None):
    """Replace or add header"""

    p = '^CONFIG_TARGET_.*=y$'
    with open(config, 'r+', encoding='utf-8') as f:
        content = re.sub(p, '', f.read(), flags=re.MULTILINE)
        if new_file:
            with open(new_file, 'w', encoding='utf-8') as fn:
                fn.write(header + content)
        else:
            f.seek(0, 0)
            f.write(header + content)


def check_device_support_single(url, define_str):
    import requests

    r = requests.get(url, timeout=3)
    if define_str in r.text:
        return True
    elif url.endswith('.mk'):
        url = url.rsplit('/', 1)[0] + '/Makefile'
        return check_device_support_single(url, define_str)
    else:
        return False


def get_shell_variables(text) -> dict:
    """Get global variables in a shell script text"""

    pattern = re.compile(r'^([a-zA-Z_][a-zA-Z0-9_]*)=(.*)$', re.MULTILINE)
    matches = pattern.findall(text)
    variables = {match[0]: match[1] for match in matches}
    return variables


def renew_shell_variables(text, variables, renews: dict) -> tuple[str, dict]:
    """Renew variables in a shell script text"""

    for k, v in renews.items():
        try:
            p_old_str = rf'^{k}={variables[k]}$'
            variables[k] = v
            text = re.sub(p_old_str, rf'{k}={v}', text, flags=re.MULTILINE)
        except KeyError:
            pass
    return text, variables


def simplify_config(config, *, backup=True, keep_header=True, ptext=False):
    save = ['# Target']
    p1 = [
        r'(CONFIG_TARGET_.*=y(?s:.*)CONFIG_LINUX_.*=y)',
        r'(# \d\. Collections(?s:.*)# end of \d\. Modules)',
        r'(# \d\. Applications(?s:.*)# end of \d\. Themes)'
    ]
    p2 = [
        r'^CONFIG_TARGET_.*=y',
        r'^# \d\.[\w ]+|^CONFIG_.*=y',
        r'^# \d\.[\w ]+|^(?:# )?CONFIG_.*'
    ]

    if backup:
        shutil.copyfile(config, config + '.fullbak')
    if not keep_header:
        p1.pop(0)
        p2.pop(0)
        save.clear()

    with open(config, encoding='utf-8') as f:
        text = f.read()

    m = re.findall('(?s:.*)'.join(p1), text)[0]
    for i, p in enumerate(p2):
        save.extend(re.findall(p, m[i], re.MULTILINE))

    text = re.sub(r'^# \d\.([\w ]+)', r'\n#\1',
                  '\n'.join(save) + '\n', flags=re.MULTILINE)
    text = re.sub(r'^\s+', '', text)

    if ptext:
        return text
    else:
        with open(config, 'w', encoding='utf-8') as f:
            f.write(text)
