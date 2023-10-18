#!/usr/bin/python3
import os
import glob
import shutil


from tools.process_text import simplify_config
from tools.routine_cmd import gen_dot_config


def main():
    destdir = os.getenv('DEPLOY_DIR').strip().rstrip('/')
    fconfig = os.getenv('DOT_CONFIG').strip()
    fclone = fconfig.split('.')[0] + '.clone.sh'

    if not os.path.exists(fce := f'{destdir}/{fclone}'):
        fce = f'{destdir}/1.clone.sh'

    with open(fcg := f'{destdir}/{fconfig}', encoding='utf-8') as f:
        text = f.readlines()
    i = 0
    s = 0
    e = 0
    for line in text:
        if all(x in line for x in ('CONFIG_TARGET_', 'DEVICE')):
            s = i + 1
        elif '# Applications' in line:
            e = i
            break
        i += 1
    for line in text[s:e]:
        if line.strip():
            break
        s += 1
    for line in reversed(text[s:e]):
        if line.strip():
            break
        e -= 1
    extra_t = None if s == e else text[s:e]

    gen_dot_config(fce, fcg)
    simplify_config(fcg, remain_text=extra_t)

    # Move .fullbak to the backups directory
    if not os.path.exists(d1 := f'{destdir}/backups'):
        os.makedirs(d1)
    shutil.move(f'{fcg}.fullbak', f'{d1}/{fconfig}.fullbak')

    # Only retain .config and .config.fullbak this time refresh
    for item in glob.glob(f'{destdir}/**', recursive=True):
        if not os.path.isdir(item) and fconfig not in item:
            os.remove(item)


if __name__ == '__main__':
    main()
