#!/usr/bin/python3
import os
import produce


if __name__ == '__main__':
    filedir = os.getenv('FILEDIR').strip().rstrip('/')
    fconfig = os.getenv('FILE').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'
    if not os.path.exists(fc1 := f'{filedir}/{fclone}'):
        fc1 = f'{filedir}/1.clone.sh'
    produce.routine_cmd(fc1, fc2 := f'{filedir}/{fconfig}')
    produce.simplify_config(fc2)
