#!/usr/bin/python3
import os
import glob
import shutil
import subprocess


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
    link = link.rstrip('@')
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
            command += f' && mv ./{path}/* ./'
        else:
            command += f' openwrt && mv ./openwrt/* ./'
    return command


# 生成模板化配置文件
def produce_conf(data: dict, prefix: str):
    # 生成clone.sh
    basecommands = produce_git_command(data["base"], True) + '\n'
    appcommands = []
    for link in data['git-app']:
        appcommands += [f'{produce_git_command(link)}\n']
    for link in data['svn-app']:
        appcommands += [f'svn export {link}\n']
    text1 = [
        '#!/bin/sh\n',
        '# 下载源码\n',
        basecommands,
        '\n',
        '# 下载插件\n',
        f'mkdir -p {(path := data["app-path"])} && cd {path}\n'
    ]
    text1 += appcommands
    with open(prefix + '.clone.sh', 'w') as f:
        f.writelines(text1)
    # 生成modify.sh
    text2 = [
        '#!/bin/sh\n',
        '# 修改登录IP\n',
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


if __name__ == '__main__':
    if not os.path.exists(destdir := os.getenv('DESTDIR', 'templet').rstrip('/')):
        os.makedirs(destdir)
    if (total := len(glob.glob(f'{destdir}/*clone.sh'))) == 0:
        serial = '1'
    else:
        if os.getenv('OVERWRITE') == 'true':
            serial = str(total)
        else:
            serial = str(total + 1)
    initfile = os.getenv('INITPATH', 'templet/init.example')
    produce_conf(initfile_format(initfile), serial)
    routine_cmd(serial + '.clone.sh', serial + '.config')
    simplify_config(serial + '.config')
    # 移动文件到目标文件夹，准备commit
    for item in glob.glob(serial + '*'):
        shutil.move(item, f'{destdir}/{item}')
