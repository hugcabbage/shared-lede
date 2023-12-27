#!/usr/bin/python3
import glob
import json
import os
import shutil
from urllib.parse import urlparse

from tools.code_summary import CodeSummary
from tools.crypt_text import crypt_str
from tools.process_text import check_device_support_single
from tools.process_text import generate_header
from tools.process_text import manifest_to_lists
from tools.process_text import modify_config_header
from tools.process_text import to_markdown_table
from tools.workflow import set_output
from tools.workflow import set_summary


def get_code_dir(clone_sh):
    with open(clone_sh, encoding='utf-8') as f:
        text = f.read()
    i = text.index('CODE_DIR=')
    j = text[i:].index('\n')
    codedir = text[i:][:j].split('=')[1]
    return codedir


def produce_temp_workfiles(headers: dict, model: str, temp: str, *, branch=None, ltag=False, ip=None, pwd=None) -> dict:
    """Generate temporary work files to make workflow easy to call,
    temp is the prefix for temporary files in the compilation process
    """

    num = num_ori = headers[model][0]
    t1, t2, t3 = headers[model][1:4]
    files = dict()

    # Generate temporary .config
    if not os.path.exists(num_ori + '.config'):
        num = '1'
    header = generate_header(headers, model)
    modify_config_header(num + '.config', header, tc1 := temp + '.config')
    files['dot_config'] = tc1

    # Generate temporary clone.sh
    if not os.path.exists(num_ori + '.clone.sh'):
        num = '1'
    with open(num + '.clone.sh', encoding='utf-8') as f:
        text = f.readlines()
    can_switch_branch = False
    for i, line in enumerate(text.copy()):
        if line.startswith('CODE_URL=') and branch:
            code = urlparse(line.split('=')[-1].strip()).path[1:].removesuffix('.git')
            subtarget_mk_url = f'https://raw.githubusercontent.com/{code}/{branch}/target/linux/{t1}/image/{t2}.mk'
            device_define_str = f'define Device/{t3}'
            if check_device_support_single(subtarget_mk_url, device_define_str):
                can_switch_branch = True
            else:
                print(f'{branch} branch does not support this model,\n'
                      f'and the branch keeps default value')
        elif line.startswith('CODE_BRANCH=') and can_switch_branch:
            text[i] = 'CODE_BRANCH=' + branch + '\n'
        elif line.startswith('SWITCH_LATEST_TAG=') and ltag:
            text[i] = 'SWITCH_LATEST_TAG=true\n'
            break
        elif i >= 10:
            break
    with open(tc2 := temp + '.clone.sh', 'w', encoding='utf-8') as f:
        f.writelines(text)
    files['clone_sh'] = tc2

    # Generate temporary modify.sh
    if not os.path.exists(num_ori + '.modify.sh'):
        num = '1'
    shutil.copyfile(num + '.modify.sh', tm1 := temp + '.modify.sh')
    spmodel = (
        'xiaomi-4a-gigabit',
        'xiaomi-3g-v2',
        'xiaomi-4a-gigabit-v2'
    )
    with open(tm1, 'a', encoding='utf-8') as f:
        if model in spmodel:
            f.write('\n. $(dirname $0)/../extra-files/modify-xiaomi-router-4a-3g-v2.sh\n')
        if ip:
            new = 'lan) ipad=${ipaddr:-"' + ip + '"} ;;'
            f.write(
                f"\nsed -i '/lan) ipad=/c{new}' package/base-files/files/bin/config_generate\n")
        if pwd:
            f.write(
                f"\nsed -i '/root/c{crypt_str(pwd)}' package/base-files/files/etc/shadow\n")
    files['modify_sh'] = tm1

    return files


def main():
    destdir = os.getenv('DEPLOY_DIR')
    temppre = os.getenv('TEMP_PREFIX')
    modelname = os.getenv('MODEL_NAME')
    branchname = os.getenv('BRANCH_NAME')
    latesttag = True if os.getenv('LATEST_TAG') == 'true' else False
    loginip = os.getenv('LOGIN_IP').strip()
    loginpwd = os.getenv('LOGIN_PWD').strip()

    os.chdir(destdir)
    with open('headers.json', encoding='utf-8') as f:
        hdata = json.load(f)
    files = produce_temp_workfiles(
        hdata, modelname, temppre, branch=branchname, ltag=latesttag, ip=loginip, pwd=loginpwd)

    print(f'The model you choose is:\n{modelname}')
    print('Temporary file paths:')
    for item in files.items():
        print(di := f'{destdir}/{item[1]}')
        set_output(item[0], di)
    set_output('codedir', get_code_dir(files['clone_sh']))


def main2():
    modelname = os.getenv('MODEL_NAME')
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

    cs = CodeSummary(codedir)
    data = cs.summary_dict
    code_name = data['code_from'].split('/')[-1]

    d1 = ['item'] + list(data.keys())
    d2 = ['content'] + list(data.values())
    for i, x in enumerate(d1.copy()):
        try:
            d1[i] = key_to_key2[x]
        except KeyError:
            continue
    data = to_markdown_table(d1, d2)
    code_data = f'<details>\n  <summary>Code Summary -> Click to expand</summary>\n\n{data}\n</details>\n'

    file = glob.glob('_collected_firmware/*.manifest')[0]
    data = manifest_to_lists(file)
    d1 = ['package'] + data[0]
    d2 = ['version'] + data[1]
    data = to_markdown_table(d1, d2)
    package_data = f'<details>\n  <summary>Package Summary -> Click to expand</summary>\n\n{data}\n</details>\n'

    stitle = f'{code_name} for {modelname.replace("-", " ")}'
    set_output('stitle', stitle)
    set_output('summary', s := f'{code_data}\n{package_data}')
    set_summary(f'## {stitle}\n\n{s}')


if __name__ == '__main__':
    if os.getenv('GITHUB_ACTION') == 'prepare-deployment':
        main()
    elif os.getenv('GITHUB_ACTION') == 'generate-summary':
        main2()
