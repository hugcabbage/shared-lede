#!/usr/bin/python3

import sys
import shutil
import fileinput

main_targets = ["mi-router-4a-gigabit","mi-router-cr6608","redmi-router-ac2100","phicomm_k2p"]
main_numbers = ["1","2","3","4"]
sub_targets = ["mi-router-cr6606","mi-router-cr6609","mi-router-3g","mi-router-4","mi-router-3-pro","mi-router-ac2100","mi-router-3g-v2"]
sub_numbers = ["2-1","2-2","2-3","2-4","2-5","3-1","1-1"]

def get_number():
    i = 1
    for target in main_targets:
        if target == sys.argv[1]:
            return i
            break
        i += 1
    else:
        j = 0
        for target in sub_targets:
            if target == sys.argv[1]:
                return sub_numbers[j]
                break
            j += 1

def copy_files(old_num,new_num,old_str,new_str):
    config_files = [".config","clone.sh","modify.sh"]
    for config_file in config_files:
        shutil.copyfile(old_num + config_file,new_num + config_file)
    for line in fileinput.input(new_num + config_files[0], inplace=1):
        line = line.replace(old_str,new_str)
        print(line, end = "")
    return

temp_num = get_number()

print(temp_num)

#复制子机型配置文件
if isinstance(temp_num,str):
    pre_num = temp_num.split("-")[0]
    m = main_numbers.index(pre_num)
    n = sub_numbers.index(temp_num)
    copy_files(pre_num,temp_num,main_targets[m],sub_targets[n])
