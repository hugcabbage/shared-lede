#!/usr/bin/python3

import os
import sys
import shutil
import fileinput

os.chdir("preset-models")

main_targets = ["mi-router-4a-gigabit", "mi-router-cr6608", "redmi-router-ac2100", "phicomm_k2p", "redmi-router-ax6s"]
main_numbers = ["1", "2", "3", "4", "5"]
sub_targets = ["mi-router-cr6606", "mi-router-cr6609", "mi-router-3g", "mi-router-4", "mi-router-3-pro", "mi-router-ac2100", "mi-router-3g-v2"]
sub_numbers = ["2-1", "2-2", "2-3", "2-4", "2-5", "3-1", "1-1"]

def get_number():
    for target in main_targets:
        if target == sys.argv[1]:
            i = main_targets.index(target)
            return main_numbers[i]
            break
    else:
        for target in sub_targets:
            if target == sys.argv[1]:
                j = sub_targets.index(target)
                return sub_numbers[j]
                break

def copy_files(old_pre, new_pre, old_str="", new_str=""):
    co_files = [".config", "clone.sh", "modify.sh"]
    for co_file in co_files:
        shutil.copyfile(old_pre + co_file, new_pre + co_file)
    if old_str != "" and new_str != "":
        for line in fileinput.input(new_pre + co_files[0], inplace=1):
            line = line.replace(old_str, new_str)
            print(line, end = "")
    return

# 获取序号
num = get_number()

print(num)

#复制子机型配置文件
if "-" in num:
    num_part1 = num.split("-")[0]
    m = main_numbers.index(num_part1)
    n = sub_numbers.index(num)
    copy_files(num_part1, "temp.", main_targets[m], sub_targets[n])
else:
    copy_files(num, "temp.")
os.rename("temp..config", "temp.config")
