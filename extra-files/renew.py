#!/usr/bin/python3
import glob
import os
import shutil

from tools.process_text import check_header_existence
from tools.process_text import generate_header
from tools.process_text import modify_config_header
from tools.process_text import simplify_config
from tools.routine_cmd import gen_dot_config


def main():
    destdir = os.getenv('DEPLOY_DIR').strip().rstrip('/')
    fconfig = os.getenv('DOT_CONFIG').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'

    fce = f'{destdir}/{fclone}' if os.path.exists(f'{destdir}/{fclone}') else f'{destdir}/1.clone.sh'
    fcg = f'{destdir}/{fconfig}'
    has_header = check_header_existence(fcg)

    if not has_header:
        sample = {'xiaomi-ac2100': ['xx', 'ramips', 'mt7621', 'xiaomi_mi-router-ac2100']}
        modify_config_header(fcg, generate_header(sample, 'xiaomi-ac2100'))

    gen_dot_config(fce, fcg)
    simplify_config(fcg, keep_header=has_header)

    # Move .fullbak to the backups directory
    os.makedirs(bas := f'{destdir}/backups', exist_ok=True)
    shutil.move(f'{fcg}.fullbak', f'{bas}/{fconfig}.fullbak')

    # Only .config and .config.fullbak of this renew are kept
    #for item in glob.glob(f'{destdir}/**', recursive=True):
    #    if not os.path.isdir(item) and fconfig not in item:
    #        os.remove(item)


if __name__ == '__main__':
    main()
