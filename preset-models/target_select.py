#!/usr/bin/python3


import os
import sys
import shutil


headers = {
    'xiaomi-4a-gigabit': ('1', 'ramips', 'mt7621', 'mi-router-4a-gigabit'),
    'xiaomi-3g-v2': ('1-1', 'ramips', 'mt7621', 'mi-router-3g-v2'),
    'xiaomi-cr6608': ('2', 'ramips', 'mt7621', 'mi-router-cr6608'),
    'xiaomi-cr6606': ('2-1', 'ramips', 'mt7621', 'mi-router-cr6606'),
    'xiaomi-cr6609': ('2-2', 'ramips', 'mt7621', 'mi-router-cr6609'),
    'xiaomi-3g': ('2-3', 'ramips', 'mt7621', 'mi-router-3g'),
    'xiaomi-4': ('2-4', 'ramips', 'mt7621', 'mi-router-4'),
    'xiaomi-3-pro': ('2-5', 'ramips', 'mt7621', 'mi-router-3-pro'),
    'redmi-ac2100': ('3', 'ramips', 'mt7621', 'redmi-router-ac2100'),
    'xiaomi-ac2100': ('3-1', 'ramips', 'mt7621', 'mi-router-ac2100'),
    'phicomm-k2p': ('4', 'ramips', 'mt7621', 'phicomm_k2p'),
    'redmi-ax6s': ('5', 'ramips', 'mt7621', 'redmi-router-ax6s')
}


# model为机型名称, num为原始配置文件前缀(即编号)，temp为即将用于编译流程中的临时文件前缀
def produce_temp_files(model: str, num: str, temp: str):
    header = [
        f'CONFIG_TARGET_{(t1 := headers[model][1])}=y\n',
        f'CONFIG_TARGET_{t1}_{(t2 := headers[model][2])}=y\n',
        f'CONFIG_TARGET_{t1}_{t2}_DEVICE_{headers[model][3]}=y\n'
    ]
    # 生成临时clone.sh, modify.sh
    shutil.copyfile(num + 'clone.sh', temp + 'clone.sh')
    shutil.copyfile(num + 'modify.sh', temp + 'modify.sh')
    # 生成临时.config
    tindex = ()
    with open(num + '.config') as f:
        text = f.readlines()
    for (index, value) in enumerate(text):
        if 'CONFIG_TARGET' in value:
            tindex += (index,)
    if len(tindex) == 0:
        text = header + text
    else:
        for i in range(3):
            text[tindex[i]] = header[i]
    with open(temp + '.config', 'w') as f:
        f.writelines(text)
    return


if __name__ == '__main__':
    os.chdir('preset-models')
    modelname = sys.argv[1]
    if modelname not in headers:
        print('机型信息错误，请检查')
    else:
        modelnum = headers[modelname][0].split('-')[0]
        produce_temp_files(modelname, modelnum, 'temp.')
        os.rename('temp..config', 'temp.config')
        # 输出对应机型的编号，以设置编译流程中的变量读取预设release内容
        print(headers[modelname][0])
