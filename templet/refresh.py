#!/usr/bin/python3
import os
import produce


if __name__ == '__main__':
    filedir = os.getenv('FILEDIR').strip().rstrip('/')
    fconfig = os.getenv('FILE').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'
    produce.routine_cmd(f'{filedir}/{fclone}', c1 := f'{filedir}/{fconfig}')
    produce.simplify_config(c1)
