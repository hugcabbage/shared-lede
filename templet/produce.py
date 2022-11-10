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


# 格式化文件，返回字典
def initfile_format(file: str) -> dict:
    data = {
        'board': '',
        'subtarget': '',
        'device': '',
        'device-name': '',
        'base': '',
        'app-path': '',
        'git-app': [],
        'svn-app': []
    }
    with open(file) as f:
        for line in f:
            for key in list(data.keys())[:6]:
                if line.startswith(key + ':='):
                    data[key] = line.split(':=')[1].strip()
                    break
            for key in list(data.keys())[6:]:
                if line.startswith(key + ':='):
                    data[key] += [line.split(':=')[1].strip()]
                    break
    return data


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
    basecommands = produce_git_command(data["base"], True) + '\n'
    appcommands = []
    for link in data['git-app']:
        appcommands += [f'{produce_git_command(link)}\n']
    for link in data['svn-app']:
        appcommands += [f'{produce_svn_command(link)}\n']
    text1 = [
        '#!/bin/sh\n',
        '\n# 下载源码\n',
        basecommands,
        '\n# 下载插件\n',
        f'mkdir -p {(path := data["app-path"])} && cd {path}\n'
    ]
    text1 += appcommands
    with open(prefix + '.clone.sh', 'w') as f:
        f.writelines(text1)
    # 生成modify.sh
    text2 = [
        '#!/bin/sh\n',
        '\n# 修改登录IP\n',
        'sed -i \'s/192.168.1.1/192.168.31.1/g\' package/base-files/files/bin/config_generate\n'
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
    # 生成header.json
    text4 = [
        '{\n',
        f'  "{(t4 := data["device-name"])}": ["{prefix}", "{t1}", "{t2}", "{t3}"]\n',
        '}\n'
    ]
    with open(prefix + '.header.json', 'w') as f:
        f.writelines(text4)
    # 生成release.yml
    text5 = [
        f'model_{t4}:\n',
        '  title: <source> for <device>\n',
        '  body:\n',
        '    - <设备><源码>固件\n',
        '    - 版本：xxx\n',
        '    - 登陆信息：<IP>，<密码>\n',
        '    - 应用：xxx\n'
    ]
    with open(prefix + '.release.yml', 'w') as f:
        f.writelines(text5)


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
    he1 = f'{destdir}/headers'
    wf1 = f'{rp1}/.github/workflows'
    if os.getenv('DELETE_ALL') == 'true':
        if dd1 != 'templet':
            if (len(glob.glob(f'{destdir}/*clone.sh'))) > 0:
                shutil.rmtree(destdir, ignore_errors=True)
            else:
                sys.exit()
        else:
            shutil.rmtree(ba1, ignore_errors=True)
            shutil.rmtree(he1, ignore_errors=True)
            for item in glob.glob(f'{destdir}/[0-9].*'):
                os.remove(item)
        for item in glob.glob(f'{wf1}/[0-9].build*'):
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
            os.remove(f'{wf1}/{serial}.build.yml')
        sys.exit()
    os.makedirs(ba1, exist_ok=True)
    os.makedirs(he1, exist_ok=True)
    serial = get_serial(destdir)
    initfile = rp1 + '/' + os.getenv('INITFILE')
    produce_conf(initfile_format(initfile), serial)
    routine_cmd(serial + '.clone.sh', serial + '.config')
    simplify_config(serial + '.config')
    # 移动文件到目标文件夹，准备commit
    for item in glob.glob(serial + '*'):
        if item.endswith('config.fullbak'):
            shutil.move(item, f'{ba1}/{item}')
        elif item.endswith('header.json'):
            shutil.move(item, f'{he1}/{item}')
        else:
            shutil.move(item, f'{destdir}/{item}')
    shutil.copyfile(f'{rp1}/templet/build.yml.example', by1 := f'{wf1}/{serial}.build.yml')
    subprocess.run(f"sed -i 's/name: xxxxxx/name: device {serial}/' {by1}", shell=True)
    subprocess.run(f"sed -i 's/SERIAL_NU: xxxxxx/SERIAL_NU: {serial}/' {by1}", shell=True)
    subprocess.run(f"sed -i 's/DEPLOYDIR: xxxxxx/DEPLOYDIR: {dd1}/' {by1}", shell=True)


if __name__ == '__main__':
    main()
