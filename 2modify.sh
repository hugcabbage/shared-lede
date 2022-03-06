#!/bin/sh
#新增机型预留脚本

#修改登录IP
sed -i 's/192.168.1.1/192.168.31.1/g' package/base-files/files/bin/config_generate