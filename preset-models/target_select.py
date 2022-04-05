#!/usr/bin/python3

import sys
import shutil
import fileinput
 
models = ["xiaomi-4a-gigabit","xiaomi-cr6608","redmi-ac2100"]
sub_models = ["xiaomi-cr6606","xiaomi-cr6609","xiaomi-3g","xiaomi-4","xiaomi-ac2100","xiaomi-3g-v2"]
sub_numbers = ["2-1","2-2","2-3","2-4","3-1","1-1"]

def copy_files(old_num,new_num,old_str,new_str):
    config_files = [".config","clone.sh","modify.sh"]
    for config_file in config_files:
        if new_num + config_file != "1-1modify.sh":
            shutil.copyfile(old_num + config_file,new_num + config_file)
            for line in fileinput.input(new_num + config_files[0], inplace=1):
                line = line.replace(old_str,new_str)
                print(line, end = "")
    return

def get_number():
    i = 1
    for target in models:
        if target == sys.argv[1]:
            return i
            break
        i += 1
    else:
        j = 0
        for target in sub_models:
            if target == sys.argv[1]:
                return sub_numbers[j]
                break
            j += 1

if sys.argv[1] == "xiaomi-cr6606":
    copy_files("2","2-1","mi-router-cr6608","mi-router-cr6606")
elif sys.argv[1] == "xiaomi-cr6609":
    copy_files("2","2-2","mi-router-cr6608","mi-router-cr6609")
elif sys.argv[1] == "xiaomi-3g":
    copy_files("2","2-3","mi-router-cr6608","mi-router-3g")
elif sys.argv[1] == "xiaomi-4":
    copy_files("2","2-4","mi-router-cr6608","mi-router-4")
elif sys.argv[1] == "xiaomi-ac2100":
    copy_files("3","3-1","redmi-router-ac2100","mi-router-ac2100")
elif sys.argv[1] == "xiaomi-3g-v2":
    copy_files("1","1-1","mi-router-4a-gigabit","mi-router-3g-v2")

print(get_number())
