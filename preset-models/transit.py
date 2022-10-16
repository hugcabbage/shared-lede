#!/usr/bin/python3


import os
import sys
import shutil


import yaml
import pandas as pd


import headers


# model为机型名称, temp为即将用于编译流程中的临时文件前缀
def produce_temp_workfiles(model: str, temp: str):
    num = headers.Headers[model][0]
    header = [
        f'CONFIG_TARGET_{(t1 := headers.Headers[model][1])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := headers.Headers[model][2])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{headers.Headers[model][3]}=y\n'
    ]
    # 生成临时clone.sh, modify.sh
    shutil.copyfile(num + 'clone.sh', temp + 'clone.sh')
    shutil.copyfile(num + 'modify.sh', temp + 'modify.sh')
    # 生成临时.config
    inxall = ()
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
    with open(temp.rstrip('.') + '.config', 'w') as f:
        f.writelines(text)
    return


# model为机型名称, release为release文档(yaml格式)路径, temp为即将用于编译流程中的临时文件前缀
def produce_release_text(model: str, release: str, temp: str):
    # 生成临时.release
    with open(release, encoding='utf-8') as f:
        text = yaml.safe_load(f)['model_' + model]
    text = pd.Series([text['title']] + text['body']) + '\n'
    with open(temp.rstrip('.') + '.release', 'w', encoding='utf-8') as f:
        f.writelines(text)


if __name__ == '__main__':
    os.chdir('preset-models')
    modelname = sys.argv[1]
    if modelname not in headers.Headers:
        print('机型信息错误，请检查')
    else:
        produce_temp_workfiles(modelname, temppre := 'temp.')
        produce_release_text(modelname, 'release.yml', temppre)
        # 输出各临时文件路径
        files = ['clone.sh', 'modify.sh', 'config', 'release']
        for x in files:
            print('preset-models/' + temppre + x)
