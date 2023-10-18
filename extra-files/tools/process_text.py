"""Text processing"""
import os
import sys
import json


def mlength(seq) -> int:
    """Get the length of the longest element in the sequence"""

    lengths = []
    for item in seq:
        if isinstance(item, (list, tuple)):
            mitem = mlength(item)
            lengths.append(mitem)
        else:
            lengths.append(len(str(item)))

    return max(lengths)


def rectangles(*lists) -> tuple[list, list]:
    """Get the length (number of elements) and 
    width (length of the longest element) of multiple lists
    """

    lengths = []
    widths = []
    for lst in lists:
        lengths.append(len(lst))
        widths.append(mlength(lst))
    return lengths, widths


def to_markdown_table(*lists) -> str:
    """Convert multiple lists to markdown tables"""

    # Calculate the maximum width of each column and determine whether all columns have the same length
    col_lengths, col_widths = rectangles(*lists)
    if len(set(col_lengths)) != 1:
        print('The list length is not uniform')
        sys.exit()

    # Create table header
    header = '|' + '|'.join(str(lst[0]).center(col_widths[i])
                            for i, lst in enumerate(lists)) + '|\n'
    separator = '|' + \
        '|'.join('-' * (col_widths[i]) for i in range(len(lists))) + '|\n'

    # Create table content
    rows = ''
    for i in range(1, col_lengths[0]):
        row = '|'
        for j, lst in enumerate(lists):
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


def manifest_to_lists(file: str) -> tuple[list, list]:
    """Convert manifest file into two lists"""

    if not os.path.isfile(file):
        print(f'Error: {file} does not exist.')
        sys.exit()

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    package = []
    version = []
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) != 2:
            print(f'Error: invalid line format -> {line}')
            continue
        if parts[0] == 'kernel':
            parts[1] = parts[1][:-26]
        if parts[0].startswith('kmod-'):
            continue
        if parts[0].startswith('lib'):
            continue
        if 'i18n' in parts[0]:
            continue
        if 'lib-' in parts[0]:
            continue
        if 'mod-' in parts[0]:
            continue
        package.append(parts[0])
        version.append(parts[1])

    return package, version


def xlsx_to_dict(file) -> dict:
    """convert xlsx file to dict"""
    from openpyxl import load_workbook

    wb = load_workbook(file)
    sheet = wb.active
    dict_data = {}

    # exclude title row, first column is key, convert other columns to list as value
    for i in range(2, sheet.max_row + 1):
        key = sheet.cell(row=i, column=1).value
        value = []
        for j in range(2, sheet.max_column + 1):
            value.append(sheet.cell(row=i, column=j).value)
        dict_data[key] = value

    return dict_data


def dict_to_json(dict_data, file):
    """convert dict data to json file, apply to header.json"""

    json_str = json.dumps(dict_data, indent=2)

    # make key and value be one line
    json_str = json_str.replace('[\n    ', '[').replace(
        ',\n    ', ', ').replace('"\n  ', '"')
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json_str)
    print('json file saved')


def simplify_config(file: str, *, backup=True, remain_text=None):
    """Simplify .config file, keep only applications and themes"""

    inxheader = ()
    inxapp = ()
    inxtheme = ()
    header_flag = True
    with open(file, encoding='utf-8') as f:
        text = f.readlines()
    if backup:
        with open(file + '.fullbak', 'w', encoding='utf-8') as f:
            f.writelines(text)
    for (index, value) in enumerate(text):
        if value.startswith('CONFIG_TARGET') and '=y' in value and header_flag:
            inxheader += (index,)
            if len(inxheader) == 3:
                header_flag = False
        elif '. Applications' in value:
            inxapp += (index,)
        elif '. Themes' in value:
            inxtheme += (index,)
    header = ['# Target\n']
    for i in inxheader:
        header += [text[i]]
    apps = list(filter(lambda x: x.strip(
        '#\n') and '# Configuration' not in x and '# end of' not in x, text[inxapp[0]:inxapp[1]]))
    apps = list(
        map(lambda x: '# Applications\n' if '. Applications' in x else x, apps))
    themes = list(filter(lambda x: x.strip('#\n')
                  and '# end of' not in x, text[inxtheme[0]:inxtheme[1]]))
    themes = list(
        map(lambda x: '# Themes\n' if '. Themes' in x else x, themes))
    for part in header, apps:
        part.append('\n')
    if remain_text:
        remain_text.append('\n')
        text = header + remain_text + apps + themes
    else:
        text = header + apps + themes
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(text)
