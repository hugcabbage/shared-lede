#!/usr/bin/python3
import os
import glob
import shutil


def move_multi_files(src, dest):
    for root, dirs, files in os.walk(src):
        for name in files:
            fullpath = os.path.join(root, name)
            shutil.move(fullpath, dest + name)


if __name__ == '__main__':
    srcdir = os.getenv('ARTIFACTDIR').rstrip('/') + '/'
    destdir = os.getenv('FILEDIR').rstrip('/') + '/'
    move_multi_files(srcdir, destdir)
    if not os.path.exists(d1 := destdir + 'backups'):
        os.makedirs(d1)
    # 移动文件到目标文件夹，准备commit
    for item in glob.glob(destdir + '*.fullbak'):
        shutil.move(item, d1 + '/' + item.split('/')[-1])
