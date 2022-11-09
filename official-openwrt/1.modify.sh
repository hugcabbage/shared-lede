#!/bin/sh

#修改登录IP
#sed -i 's/192.168.1.1/192.168.10.1/g' package/base-files/files/bin/config_generate

#复制uci-defaults脚本
mkdir -p files/etc/uci-defaults
cp $DEPLOYDIR/uci-scripts/* files/etc/uci-defaults/

#更改默认包
sed -i 's/dnsmasq/dnsmasq-full/g' include/target.mk
