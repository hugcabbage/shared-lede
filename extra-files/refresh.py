#!/usr/bin/python3
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)) + '/templet')
import produce


if __name__ == '__main__':
    destdir = os.getenv('DEPLOYDIR').strip().rstrip('/')
    fconfig = os.getenv('FILE').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'
    if not os.path.exists(fc1 := f'{destdir}/{fclone}'):
        fc1 = f'{destdir}/1.clone.sh'
    with open(fc1) as f:
        text = f.readlines()
    for t in text:
        if 'openwrt/openwrt' in t:
            offi = True
            break
    else:
        offi = False
    produce.routine_cmd(fc1, fc2 := f'{destdir}/{fconfig}')
    produce.simplify_config(fc2, offi)
