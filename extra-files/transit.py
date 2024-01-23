#!/usr/bin/python3
import glob
import json
import os
import re
import shutil
from urllib.parse import urlparse

from tools.code_summary import CodeSummary
from tools.color import *
from tools.crypt_text import crypt_str
from tools.process_text import check_device_support_single
from tools.process_text import check_header_existence
from tools.process_text import generate_header
from tools.process_text import get_shell_variables
from tools.process_text import manifest_to_lists
from tools.process_text import modify_config_header
from tools.process_text import renew_shell_variables
from tools.process_text import to_markdown_table
from tools.workflow import set_output
from tools.workflow import set_summary


def switch_branch_or_tag(headers, model, text, variables, branch, ltag):
    renews = dict()
    url_frame = 'https://raw.githubusercontent.com/{code}/{branch}/target/linux/{t1}/image/{t2}.mk'
    define_frame = 'define Device/{t3}'

    if branch:
        try:
            code = urlparse(variables['CODE_URL']).path[1:].removesuffix('.git')
            arguments = dict(zip(
                ('code', 'branch', 't1', 't2', 't3'),
                (code, branch, *headers[model][1:4])))
        except TypeError:
            # If hearders is None, switch the branch directly
            # without checking if the branch supports the device
            renews['CODE_BRANCH'] = branch
        else:
            mk_url = url_frame.format(**arguments)
            define_str = define_frame.format(**arguments)
            if check_device_support_single(mk_url, define_str):
                renews['CODE_BRANCH'] = branch
            else:
                print(red(f"{branch} doesn't support this model,\nand the branch keeps default value"))

    if ltag:
        renews['SWITCH_LATEST_TAG'] = 'true'

    return renew_shell_variables(text, variables, renews)


def generate_temp_config(headers, model, temp, ori):
    file = ori + '.config'
    if not os.path.exists(file):
        raise FileNotFoundError(red(f'{file} not found'))
    if headers:
        header = generate_header(headers, model)
        modify_config_header(file, header, tc1 := temp + '.config')
    else:
        if not check_header_existence(file):
            raise RuntimeError(red(f'{file} has no "CONFIG_TARGET_" string'))
        shutil.copyfile(file, tc1 := temp + '.config')
    return tc1


def generate_temp_clone_sh(headers, model, temp, ori, branch, ltag):
    num = ori if os.path.exists(ori + '.clone.sh') else '1'
    with open(num + '.clone.sh', encoding='utf-8') as f:
        text = f.read()
    variables = get_shell_variables(text)
    if branch or ltag:
        text, variables = switch_branch_or_tag(headers, model, text, variables, branch, ltag)
    with open(tc2 := temp + '.clone.sh', 'w', encoding='utf-8') as f:
        f.write(text)
    return tc2, variables


def generate_temp_modify_sh(temp, ori, config, ip, pwd):
    num = ori if os.path.exists(ori + '.modify.sh') else '1'
    shutil.copyfile(num + '.modify.sh', tm1 := temp + '.modify.sh')

    pattern = re.compile(
        r'^CONFIG_TARGET_.*DEVICE_xiaomi_mi-router-(?:3g-v2|4a-gigabit)(?:-v2)?=y$',
        re.MULTILINE)
    with open(config, encoding='utf-8') as f:
        c_text = f.read()
    with open(tm1, 'a', encoding='utf-8') as f:
        if pattern.search(c_text):
            f.write('\n. $(dirname $0)/../extra-files/modify-xiaomi-router-4a-3g-v2.sh\n')
        if ip:
            new = 'lan) ipad=${ipaddr:-"' + ip + '"} ;;'
            f.write(
                f"\nsed -i '/lan) ipad=/c{new}' package/base-files/files/bin/config_generate\n")
        if pwd:
            f.write(
                f"\nsed -i '/root/c{crypt_str(pwd)}' package/base-files/files/etc/shadow\n")
    return tm1


def produce_temp_workfiles(
        workdir: str,
        model: str,
        temp: str = '_temp',
        *,
        branch=None,
        ltag=False,
        ip=None,
        pwd=None):
    """Generate temporary work files to make workflow easy to call,
    temp is the prefix for temporary files in the compilation process
    """

    prev_path = os.getcwd()
    os.chdir(workdir)
    cur_path = os.getcwd()
    files = dict()

    with open('headers.json', encoding='utf-8') as f:
        headers = json.load(f)
    try:
        num_ori = headers[model][0]
    except KeyError:
        num_ori = model
        headers = None

    files['dot_config'] = os.path.join(
        cur_path, generate_temp_config(headers, model, temp, num_ori))

    clone_sh, variables = generate_temp_clone_sh(headers, model, temp, num_ori, branch, ltag)
    files['clone_sh'] = os.path.join(cur_path, clone_sh)

    files['modify_sh'] = os.path.join(
        cur_path, generate_temp_modify_sh(temp, num_ori, files['dot_config'], ip, pwd))

    os.chdir(prev_path)
    return files, variables


def main():
    destdir = os.getenv('DEPLOY_DIR')
    temppre = os.getenv('TEMP_PREFIX')
    model = os.getenv('MODEL_NAME') or os.getenv('MULTI_CONFIG').removesuffix('.config')
    branch = os.getenv('BRANCH_NAME')
    latesttag = True if os.getenv('LATEST_TAG') == 'true' else False
    loginip = os.getenv('LOGIN_IP', '').strip()
    loginpwd = os.getenv('LOGIN_PWD', '').strip()

    files, variables = produce_temp_workfiles(
        destdir, model, temppre, branch=branch, ltag=latesttag, ip=loginip, pwd=loginpwd)

    fordevice = model.replace('-', ' ')
    print(
        'The device you choose is:',
        green(fordevice),
        'Temporary file paths:',
        sep='\n'
    )
    for k, v in files.items():
        print(v)
        set_output(k, v)

    set_output('fordevice', fordevice)
    set_output('codedir', variables['CODE_DIR'])


def main2():
    fordevice = os.getenv('FOR_DEVICE')
    codedir = os.getenv('CODE_DIR')

    key_to_key2 = {
        'code_from': 'code',
        'code_branch': 'version',
        'code_tag': 'version number',
        'code_commit_hash': 'commit hash',
        'code_commit_date': 'commit date',
        'build_date': 'build date',
        'login_ip': 'login ip',
        'login_user': 'login user',
        'login_pwd': 'login password',
        'arch_packages': 'arch packages'
    }

    summary = ''
    cs = CodeSummary(codedir)
    data1 = cs.summary_dict
    code_name = data1['code_from'].split('/')[-1]

    d1 = ['item'] + list(data1.keys())
    d2 = ['content'] + list(data1.values())
    for i, x in enumerate(d1.copy()):
        try:
            d1[i] = key_to_key2[x]
        except KeyError:
            continue
    data1 = to_markdown_table(d1, d2)
    summary += f'<details>\n  <summary>Code Summary -> Click to expand</summary>\n\n{data1}\n</details>\n'

    try:
        file = glob.glob('_collected_firmware/*.manifest')[0]
    except IndexError:
        print(red("Error: can't find manifest file"))
    else:
        data2 = manifest_to_lists(file)
        d1 = ['package'] + data2[0]
        d2 = ['version'] + data2[1]
        data2 = to_markdown_table(d1, d2)
        summary += f'\n<details>\n  <summary>Package Summary -> Click to expand</summary>\n\n{data2}\n</details>\n'

    stitle = f'{code_name} for {fordevice}'
    set_output('stitle', stitle)
    set_output('summary', summary)
    set_summary(f'## {stitle}\n\n{summary}')


if __name__ == '__main__':
    if os.getenv('GITHUB_ACTION') == 'prepare-deployment':
        main()
    elif os.getenv('GITHUB_ACTION') == 'generate-summary':
        main2()
