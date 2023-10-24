#!/usr/bin/python3
import os
import glob
import json
import shutil


from tools.code_summary import CodeSummary
from tools.crypt_text import crypt_str
from tools.process_text import manifest_to_lists
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


def produce_temp_workfiles(headers: dict, model: str, temp: str, *, ip=None, pwd=None) -> dict:
    """Generate temporary work files to make workflow easy to call
    headers is the model data
    model is a model name
    temp is the prefix for temporary files in the compilation process
    """

    num = headers[model][0]
    files = {}

    # Generate temporary .config
    hindex = []
    header = [
        f'CONFIG_TARGET_{(t1 := headers[model][1])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := headers[model][2])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{headers[model][3]}=y\n'
    ]
    with open(num + '.config', encoding='utf-8') as f:
        text = f.readlines()
    for index, value in enumerate(text):
        if value.startswith('CONFIG_TARGET') and '=y' in value:
            hindex.append(index)
            if len(hindex) == 3:
                break
    if len(hindex) == 0:
        text = header + text
    else:
        for i in range(3):
            text[hindex[i]] = header[i]
    with open(tc1 := temp + '.config', 'w', encoding='utf-8') as f:
        f.writelines(text)
    files['dot_config'] = tc1

    # Generate temporary clone.sh
    if not os.path.exists(num + '.clone.sh'):
        num = '1'
    with open(num + '.clone.sh', encoding='utf-8') as f:
        text = f.readlines()
        if os.getenv('SWITCH_TAG') == 'true':
            for i, line in enumerate(text.copy()):
                if line.startswith('SWITCH_TAG_FLAG='):
                    text[i] = 'SWITCH_TAG_FLAG=true\n'
                    break
    with open(tc2 := temp + '.clone.sh', 'w', encoding='utf-8') as f:
        f.writelines(text)
    files['clone_sh'] = tc2

    # Generate temporary modify.sh
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
    loginip = os.getenv('LOGIN_IP').strip()
    loginpwd = os.getenv('LOGIN_PWD').strip()

    os.chdir(destdir)
    with open('headers.json', encoding='utf-8') as f:
        hdata = json.load(f)
    files = produce_temp_workfiles(
        hdata, modelname, temppre, ip=loginip, pwd=loginpwd)

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
