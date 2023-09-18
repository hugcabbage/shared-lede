#!/usr/bin/python3
import os
import json
import shutil


import yaml


from tools.crypt import crypt_root


# headers为机型数据, model为机型名称, temp为即将用于编译流程中的临时文件前缀
def produce_temp_workfiles(headers: dict, model: str, temp: str , * , loginip=None, loginpwd=None):
    num = headers[model][0]
    # 生成临时.config
    inxall = ()
    header = [
        f'CONFIG_TARGET_{(t1 := headers[model][1])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := headers[model][2])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{headers[model][3]}=y\n'
    ]
    with open(num + '.config') as f:
        text = f.readlines()
    for (index, value) in enumerate(text):
        if value.startswith('CONFIG_TARGET') and '=y' in value:
            inxall += (index,)
            if len(inxall) == 3:
                break
    if len(inxall) == 0:
        text = header + text
    else:
        for i in range(3):
            text[inxall[i]] = header[i]
    with open(tc1 := temp + '.config', 'w') as f:
        f.writelines(text)
    # 生成临时clone.sh
    if not os.path.exists(num + '.clone.sh'):
        num = '1'
    shutil.copyfile(num + '.clone.sh', tc2 := temp + '.clone.sh')
    # 生成临时modify.sh
    shutil.copyfile(num + '.modify.sh', tm1 := temp + '.modify.sh')
    with open(tm1, 'a') as f:
        if model == 'xiaomi-4a-gigabit' or model == 'xiaomi-3g-v2' or model == 'xiaomi-4a-gigabit-v2':
            f.write('\n. extra-files/modify-xiaomi-router-4a-3g-v2.sh\n')
        if loginip:
            new = 'lan) ipad=${ipaddr:-"' + loginip + '"} ;;'
            f.write(f"\nsed -i '/lan) ipad=/c{new}' package/base-files/files/bin/config_generate\n")
        if loginpwd:
            f.write(f"\nsed -i '/root/c{crypt_root(loginpwd)}' package/base-files/files/etc/shadow\n")
    return tc1, tc2, tm1


# model为机型名称, release为release文档(yaml格式)路径, temp为即将用于编译流程中的临时文件前缀
def produce_release_text(model: str, release: str, temp: str):
    # 生成临时.release
    with open(release, encoding='utf-8') as f:
        if (m1 := 'model_' + model) in (y1 := yaml.safe_load(f)):
            text = y1[m1]['title'] + '\n' + '\n'.join(y1[m1]['body']) + '\n'
        else:
            text = f'{model.replace("-", " ")}\n' + \
                '无更多信息，预设请编辑release.yml\n'
    with open(tr1 := temp + '.release', 'w', encoding='utf-8') as f:
        f.write(text)
    return tr1


def main():
    destdir = os.getenv('DEPLOYDIR')
    modelname = os.getenv('MODEL_NAME')
    temppre = os.getenv('TEMP_PREFIX')
    try:
        lip = os.getenv('LOGIN_IP').strip()
    except:
        lip = None
    try:
        lpwd = os.getenv('LOGIN_PWD').strip()
    except:
        lpwd = None
    os.chdir(destdir)
    with open('headers.json') as f:
        hdata = json.load(f)
    if modelname not in hdata:
        print('机型信息错误，请检查')
    else:
        files = produce_temp_workfiles(hdata, modelname, temppre, loginip=lip, loginpwd=lpwd) + \
            (produce_release_text(modelname, 'release.yml', temppre),)
        # 输出选择的机型与各临时文件路径
        print('你选择的机型为：' + '\n' + modelname)
        print('各临时文件路径：')
        for item in files:
            print(f'{destdir}/{item}')
    return


if __name__ == '__main__':
    main()
