#!/bin/sh

# modify login IP
#sed -i 's/192.168.1.1/192.168.10.1/g' package/base-files/files/bin/config_generate

# copy uci-defaults script(s)
mkdir -p files/etc/uci-defaults
cp $(dirname $0)/uci-scripts/* files/etc/uci-defaults/

# modify default package(s)
sed -i 's/dnsmasq/dnsmasq-full/g' include/target.mk
