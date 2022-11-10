#!/bin/sh

#修改登录IP
sed -i 's/192.168.1.1/192.168.31.1/g' package/base-files/files/bin/config_generate

#修改主机名
#sed -i 's/OpenWrt/Xiaomi-Router/g' package/base-files/files/bin/config_generate

#删除自带低版本xray-core
rm -rf feeds/packages/net/xray-core
rm -rf package/feeds/packages/xray-core

#复制smartdns配置
rm -rf feeds/packages/net/smartdns
rm -rf package/feeds/packages/net/smartdns
cp -r extra-files/smartdns feeds/packages/net/

#复制uci-defaults脚本
mkdir -p files/etc/uci-defaults
cp $DEPLOYDIR/uci-scripts/* files/etc/uci-defaults/

#设置WIFI
#sed -i 's/OpenWrt/coolxiaomi/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i 's/wireless.default_radio${devidx}.encryption=none/wireless.default_radio${devidx}.encryption=psk-mixed/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i '/encryption/a\set wireless.default_radio${devidx}.key=coolxiaomi' package/kernel/mac80211/files/lib/wifi/mac80211.sh

#修改登录密码为coolxiaomi
#sed -i '/root/croot:$1$CBd7u73H$LvSDVXLBrzpk4JfuuN.Lv1:18676:0:99999:7:::' package/base-files/files/etc/shadow

#删除一些zzz中的命令
ZZZ_PATH='package/default-settings/files/zzz-default-settings'
sed -i -e '/DISTRIB_/d' -e '/footer.htm/d' -e '/admin_status/d' $ZZZ_PATH

#替换geodata源
. extra-files/update-geodata.sh
