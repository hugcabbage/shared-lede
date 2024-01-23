#!/usr/bin/python3
import glob
import os
import re
import shutil
import sys

import toml

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'extra-files'))
from tools.color import *
from tools.crypt_text import crypt_str
from tools.process_text import generate_header
from tools.process_text import simplify_config
from tools.routine_cmd import gen_dot_config


def produce_git_command(link: str, isbase=False) -> str:
    """Produce git command by link"""

    segments = link.strip().rstrip('@').split('@')
    url = segments[0]
    branch = segments[1] if len(segments) > 1 else ''
    path = segments[2] if len(segments) > 2 else ('_firmware_code' if isbase else '')

    branch_part = f' -b {branch}' if branch else ''
    path_part = f' {path}' if path else ''

    if isbase:
        command = (
            f'CODE_DIR={path}\n'
            f'git clone --single-branch{branch_part} {url}{path_part}\n'
            'mv ./$CODE_DIR/* ./')
    else:
        command = f'git clone --depth 1{branch_part} {url}{path_part}'

    return command


def produce_svn_command(link: str) -> str:
    """Produce svn command by link"""

    link = link.strip().rstrip('@')
    segments = link.split('@')
    url = segments[0]
    path = segments[1] if len(segments) > 1 else ''
    command = f'svn export {url} {path}'

    return command


def produce_conf(data: dict, prefix: str):
    """Generate template-based configuration files"""

    required_keys = ['board', 'subtarget', 'device', 'base']
    if not all(data.get(key) for key in required_keys):
        sys.exit('missing required key(s)')

    # Generate clone.sh
    base_command = produce_git_command(data['base'], True) + '\n'
    app_commands, dl_app_text = '', ''

    for link in data.get('git_app', ''):
        app_commands += f'{produce_git_command(link)}\n'
    for link in data.get('svn_app', ''):
        app_commands += f'{produce_svn_command(link)}\n'

    if app_commands:
        app_path = data.get('app_path', '')
        if not re.match(r'package(/|$)', app_path):
            app_path = 'package/_supply_packages'
        dl_app_text = (
            f'\n# download app codes\n'
            f'mkdir -p {app_path} && cd {app_path}\n'
            f'{app_commands}')

    clone_text = (
        '#!/usr/bin/env bash\n'
        '\n# download base code\n'
        f'{base_command}'
        f'{dl_app_text}')

    with open(prefix + '.clone.sh', 'w', encoding='utf-8') as f:
        f.write(clone_text)

    # Generate modify.sh
    modify_text = (
        '#!/usr/bin/env bash\n'
        '\n# modify login IP\n')
    login_ip = data.get('login_ip')
    if login_ip:
        modify_text += (
            f'sed -i \'s/192.168.1.1/{login_ip}/g\' package/base-files/files/bin/config_generate\n')
    else:
        modify_text += (
            '#sed -i \'s/192.168.1.1/192.168.51.1/g\' package/base-files/files/bin/config_generate\n')

    login_pwd = data.get('login_pwd')
    if login_pwd:
        modify_text += (
            f'\n# modify login password to {login_pwd}\n'
            f"sed -i '/root/c{crypt_str(login_pwd)}' package/base-files/files/etc/shadow\n")
    else:
        modify_text += (
            '\n# modify login password to 888888\n'
            f"#sed -i '/root/c{crypt_str('888888')}' package/base-files/files/etc/shadow\n")

    if offi_code := 'openwrt/openwrt' in data['base']:
        modify_text += (
            '\n# copy uci-defaults script(s)\n'
            'mkdir -p files/etc/uci-defaults\n'
            'cp $(dirname $0)/../preset-openwrt/uci-scripts/17_wireless files/etc/uci-defaults/\n'
            '\n# modify default package(s)\n'
            "sed -i 's/dnsmasq/dnsmasq-full/g' include/target.mk\n")

    with open(prefix + '.modify.sh', 'w', encoding='utf-8') as f:
        f.write(modify_text)

    # Generate .config
    header_dict = {data['device_name']: [prefix, data['board'], data['subtarget'], data['device']]}
    config_text = ''.join(generate_header(header_dict, data['device_name']))

    if offi_code:
        config_text += (
            '\n# Collections\n'
            'CONFIG_PACKAGE_luci=y\n'
            '\n# Translations\n'
            'CONFIG_LUCI_LANG_zh_Hans=y\n'
            '\n# Applications\n')

    with open(prefix + '.config', 'w', encoding='utf-8') as f:
        f.write(config_text)


def get_serial(dest_dir, ow_last, ow_spec):
    """Get the serial number"""

    total = len(glob.glob(f'{dest_dir}/*clone.sh'))
    if ow_spec:
        return ow_spec
    elif ow_last:
        return str(total)
    else:
        return str(total + 1)


def delete_all(deploy_dir, dest_dir, wf_dir):
    if deploy_dir == 'templet':
        print(red('Cannot delete templet directory!'))
        sys.exit(1)
    else:
        shutil.rmtree(dest_dir, ignore_errors=True)
    for item in glob.glob(f'{wf_dir}/{deploy_dir}-[0-9]*'):
        os.remove(item)
    print(green(f'{deploy_dir} and related files have been removed!'))
    sys.exit()


def delete_some(deploy_dir, dest_dir, wf_dir, some_num):
    nums = some_num.replace(' ', '').rstrip(',').split(',')
    for root, dirs, files in os.walk(dest_dir):
        for name in files:
            if any(name.startswith(serial + '.') for serial in nums):
                os.remove(os.path.join(root, name))
    for serial in nums:
        for item in glob.glob(f'{wf_dir}/{deploy_dir}-{serial}*'):
            os.remove(item)
    print(green(f'Files related to {some_num} in {deploy_dir} have been removed!'))
    sys.exit()


def process_config(ba_dir, init_file, serial):
    os.makedirs(ba_dir, exist_ok=True)
    with open(init_file, encoding='utf-8') as f:
        init_dict = toml.load(f)
    if not init_dict.get('device_name'):
        init_dict['device_name'] = init_dict['device'].replace('-', ' ').replace('_', ' ')
    produce_conf(init_dict, serial)
    gen_dot_config(serial + '.clone.sh', serial + '.config')
    simplify_config(serial + '.config', keep_header=True)
    return init_dict


def move_files(deploy_dir, dest_dir, wf_dir, ba_dir, serial, ow_last):
    if ow_last:
        for item in glob.glob(f'{wf_dir}/{deploy_dir}-{serial}*'):
            os.remove(item)
    for item in glob.glob(serial + '*'):
        if item.endswith('config.fullbak'):
            shutil.move(item, f'{ba_dir}/{item}')
        else:
            shutil.move(item, f'{dest_dir}/{item}')


def generate_build_yml(deploy_dir, wf_dir, repo_path, init_dict, serial):
    ori_file = f'{repo_path}/templet/build.yml'
    new_file = f'{wf_dir}/{deploy_dir}-{serial}-{init_dict["device_name"].replace(" ", "-")}.yml'
    with open(ori_file, encoding='utf-8') as f1, open(new_file, 'w', encoding='utf-8') as f2:
        text = f1.read()
        replacements = {
            'xxxxxx??name': f'{deploy_dir} {init_dict["device_name"]}',
            'xxxxxx??serial': f'{serial}',
            'xxxxxx??deploy': f'{deploy_dir}',
        }
        for ori, new in replacements.items():
            text = text.replace(ori, new)
        f2.write(text)


def main():
    repo_path = os.getenv('REPO_PATH')
    deploy_dir = os.getenv('DEPLOY_DIR').strip('/ ')
    dest_dir = f'{repo_path}/{deploy_dir}'
    ba_dir = f'{dest_dir}/backups'
    wf_dir = f'{repo_path}/.github/workflows'
    init_file = f'{repo_path}/{os.getenv("INIT_FILE").strip("/ ")}'
    ow_last = True if os.getenv('OVERWRITE_LAST') == 'true' else False
    ow_spec = os.getenv('OVERWRITE_SPEC').strip()
    serial = get_serial(dest_dir, ow_last, ow_spec)

    if os.getenv('DELETE_ALL') == 'true':
        delete_all(deploy_dir, dest_dir, wf_dir)
    if ds := os.getenv('DELETE_SOME').strip():
        delete_some(deploy_dir, dest_dir, wf_dir, ds)

    init_dict = process_config(ba_dir, init_file, serial)
    move_files(deploy_dir, dest_dir, wf_dir, ba_dir, serial, ow_last)
    generate_build_yml(deploy_dir, wf_dir, repo_path, init_dict, serial)

    print(green(f'Device configuration files have been generated in {deploy_dir}!'))


if __name__ == '__main__':
    main()
