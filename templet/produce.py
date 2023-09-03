#!/usr/bin/python3
import os
import sys
import glob
import shutil
import subprocess


# 获取编号
def get_serial(directory: str):
    if (total := len(glob.glob(f'{directory}/*clone.sh'))) == 0:
        number = '1'
    else:
        if os.getenv('OVERWRITE_LAST') == 'true':
            number = str(total)
        elif (os1 := os.getenv('OVERWRITE_SPEC')) != '':
            number = str(os1)
        else:
            number = str(total + 1)
    return number


# 按链接提取应用名
def extract_app_name(links: list) -> list:
    apps = []
    for link in links:
        apps += [f'* {link.split("@")[0].split("/")[-1].rstrip(".git")}\n']
    return apps


# 按链接生成git clone命令
def produce_git_command(link: str, isbase=False) -> str:
    path = ''
    link = link.strip().rstrip('@')
    # 0个@
    if '@' not in (url := link):
        command = f'git clone --depth 1 {url}'
    else:
        segment = link.split('@')
        url = segment[0]
        # 1个@
        if link.count('@') == 1:
            branch = segment[1]
            command = f'git clone --depth 1 -b {branch} {url}'
        # 2个@
        else:
            if segment[1] == '':
                path = segment[2]
                command = f'git clone --depth 1 {url} {path}'
            else:
                branch = segment[1]
                path = segment[2]
                command = f'git clone --depth 1 -b {branch} {url} {path}'
    if isbase:
        if path != '':
            path = path.rstrip('/')
            command += f' && mv ./{path}/* ./'
        else:
            command += f' openwrt && mv ./openwrt/* ./'
    return command


# 按链接生成svn命令
def produce_svn_command(link: str) -> str:
    link = link.strip().rstrip('@')
    # 0个@
    if '@' not in (url := link):
        command = f'svn export {url}'
    # 1个@
    else:
        segment = link.split('@')
        url = segment[0]
        path = segment[1]
        command = f'svn export {url} {path}'
    return command


# 生成模板化配置文件
def produce_conf(data: dict, prefix: str):
    # 生成clone.sh
    basecommands = produce_git_command(data['base'], True) + '\n'
    appcommands = []
    for link in data['git_app']:
        appcommands += [f'{produce_git_command(link)}\n']
    for link in data['svn_app']:
        appcommands += [f'{produce_svn_command(link)}\n']
    text1 = [
        '#!/bin/sh\n',
        '\n# download base code\n',
        basecommands,
        '\n# download app codes\n',
        f'mkdir -p {(path := data["app_path"])} && cd {path}\n'
    ]
    text1 += appcommands
    with open(prefix + '.clone.sh', 'w') as f:
        f.writelines(text1)
    # 生成modify.sh
    text2 = [
        '#!/bin/sh\n',
        '\n# modify login IP\n',
        f'sed -i \'s/192.168.1.1/{data["login_ip"]}/g\' package/base-files/files/bin/config_generate\n'
    ]
    with open(prefix + '.modify.sh', 'w') as f:
        f.writelines(text2)
    # 生成.config
    text3 = [
        f'CONFIG_TARGET_{(t1 := data["board"])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := data["subtarget"])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{(t3 := data["device"])}=y\n'
    ]
    with open(prefix + '.config', 'w') as f:
        f.writelines(text3)
    # 生成release.md
    text4 = [
        f'## {data["base_name"]} for {data["device_name"]}\n',
        f'\nversion：{data["base_version"]}\n',
        '\nlogin info：\n',
        f'* IP {data["login_ip"]}\n',
        '* password default\n',
        '\napplications：\n'
    ] + extract_app_name(data['git_app']) + extract_app_name(data['svn_app'])
    with open(prefix + '.release.md', 'w') as f:
        f.writelines(text4)


# 简化.config，仅保留应用和主题
def simplify_config(file: str, backup=True):
    inxheader = ()
    inxapp = ()
    inxtheme = ()
    addflag = True
    with open(file) as f:
        text = f.readlines()
    if backup:
        with open(file + '.fullbak', 'w') as f:
            f.writelines(text)
    for (index, value) in enumerate(text):
        if value.startswith('CONFIG_TARGET') and '=y' in value and addflag:
            inxheader += (index,)
            if len(inxheader) == 3:
                addflag = False
        elif value.startswith('# 3. Applications'):
            inxapp += (index,)
        elif value.startswith('# end of 3. Applications'):
            inxapp += (index,)
        elif value.startswith('# 4. Themes'):
            inxtheme += (index,)
        elif value.startswith('# end of 4. Themes'):
            inxtheme += (index,)
    header = []
    for i in inxheader:
        header += [text[i]]
    text = header + text[inxapp[0]:inxapp[1]] + text[inxtheme[0]:inxtheme[1]]
    with open(file, 'w') as f:
        f.writelines(text)
    sedcommands = [
        f"sed -i '/^$/d' {file}",
        f"sed -i '/^#$/d' {file}",
        f"sed -i '/# Configuration/d' {file}",
        f"sed -i '/# end of 3. Applications/d' {file}",
        f"sed -i '/# end of 4. Themes/d' {file}",
        f"sed -i '/# end of Configuration/d' {file}",
        f"sed -i 's/3. Applications/Applications/g' {file}",
        f"sed -i 's/4. Themes/Themes/g' {file}",
        f"sed -i '1i # Target' {file}",
        f"sed -i '/# Applications/i \n' {file}",
        f"sed -i '/# Themes/i \n' {file}"
    ]
    for cmd in sedcommands:
        subprocess.run(cmd, shell=True)


# 执行终端命令，形参为各文件路径
def routine_cmd(clone: str, config: str):
    commands = [
        f'chmod +x {clone} && ./{clone}',
        './scripts/feeds update -a && ./scripts/feeds install -a',
        f'mv -f {config} .config && make defconfig',
        f'cp -f .config {config}'
    ]
    for cmd in commands:
        subprocess.run(cmd, shell=True)


def main():
    destdir = (rp1 := os.getenv('REPO_PATH').rstrip('/')) + '/' + (dd1 := os.getenv('DEPLOYDIR').rstrip('/'))
    ba1 = f'{destdir}/backups'
    wf1 = f'{rp1}/.github/workflows'
    if os.getenv('DELETE_ALL') == 'true':
        if dd1 != 'templet':
            if (len(glob.glob(f'{destdir}/*clone.sh'))) > 0:
                shutil.rmtree(destdir, ignore_errors=True)
            else:
                sys.exit()
        else:
            shutil.rmtree(ba1, ignore_errors=True)
            for item in glob.glob(f'{destdir}/[0-9].*'):
                os.remove(item)
        for item in glob.glob(f'{wf1}/{dd1}-[0-9]*'):
            os.remove(item)
        sys.exit()
    if (ds1 := os.getenv('DELETE_SPEC')) != '':
        ds1 = ds1.replace(' ', '').rstrip(',').split(',')
        for root, dirs, files in os.walk(destdir):
            for name in files:
                for serial in ds1:
                    if name.startswith(serial + '.'):
                        os.remove(os.path.join(root, name))
                        break
        for serial in ds1:
            os.remove(f'{wf1}/{dd1}-{serial}*')
        sys.exit()
    os.makedirs(ba1, exist_ok=True)
    serial = get_serial(destdir)
    initfile = rp1 + '/' + os.getenv('INITFILE')
    with open(initfile) as f:
        import toml
        produce_conf(tl1 := toml.load(f), serial)
    routine_cmd(serial + '.clone.sh', serial + '.config')
    simplify_config(serial + '.config')
    # 移动文件到目标文件夹，准备commit
    for item in glob.glob(serial + '*'):
        if item.endswith('config.fullbak'):
            shutil.move(item, f'{ba1}/{item}')
        else:
            shutil.move(item, f'{destdir}/{item}')
    shutil.copyfile(f'{rp1}/templet/build.yml', by1 := f"{wf1}/{dd1}-{serial}-{tl1['device_name'].replace(' ', '-')}.yml")
    subprocess.run(f"sed -i 's/name: xxxxxx/name: {dd1} {tl1['device_name']}/' {by1}", shell=True)
    subprocess.run(f"sed -i 's/SERIAL_NU: xxxxxx/SERIAL_NU: {serial}/' {by1}", shell=True)
    subprocess.run(f"sed -i 's/DEPLOYDIR: xxxxxx/DEPLOYDIR: {dd1}/' {by1}", shell=True)


if __name__ == '__main__':
    main()
