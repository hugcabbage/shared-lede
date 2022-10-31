#!/usr/bin/python3
import os
import sys
import json
import shutil


import yaml
import pandas as pd


# headers为机型数据, model为机型名称, temp为即将用于编译流程中的临时文件前缀
def produce_temp_workfiles(headers: dict, model: str, temp: str):
    num = headers[model][0]
    header = [
        f'CONFIG_TARGET_{(t1 := headers[model][1])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := headers[model][2])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{headers[model][3]}=y\n'
    ]
    # 生成临时clone.sh, modify.sh
    shutil.copyfile(num + '.clone.sh', temp + '.clone.sh')
    shutil.copyfile(num + '.modify.sh', temp + '.modify.sh')
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
    with open(temp + '.config', 'w') as f:
        f.writelines(text)
    return


# model为机型名称, release为release文档(yaml格式)路径, temp为即将用于编译流程中的临时文件前缀
def produce_release_text(model: str, release: str, temp: str):
    # 生成临时.release
    with open(release, encoding='utf-8') as f:
        if (m1 := 'model_' + model) in (y1 := yaml.safe_load(f)):
            text = y1[m1]
            text = pd.Series([text['title']] + text['body']) + '\n'
        else:
            text = [
                f'{model.replace("-", " ")}\n',
                '无更多信息，预设请编辑release.yml\n'
            ]
    with open(temp + '.release', 'w', encoding='utf-8') as f:
        f.writelines(text)


if __name__ == '__main__':
    deploydir = os.getenv('DEPLOYDIR')
    modelname = os.getenv('MODEL_NAME')
    temppre = os.getenv('TEMP_PREFIX')
    os.chdir(deploydir)
    with open('headers.json') as f:
        hdata = json.load(f)
    if modelname not in hdata:
        print('机型信息错误，请检查')
    else:
        produce_temp_workfiles(hdata, modelname, temppre)
        produce_release_text(modelname, 'release.yml', temppre)
        # 输出选择的机型与各临时文件路径
        print('你选择的机型为：' + '\n' + modelname)
        print('各临时文件路径：')
        files = ['.clone.sh', '.modify.sh', '.config', '.release']
        for item in files:
            print(f'{deploydir}/{temppre}{item}')
