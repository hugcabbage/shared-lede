#!/bin/sh
#修改登录IP
sed -i 's/192.168.1.1/192.168.31.1/g' package/base-files/files/bin/config_generate
#修改主机名
sed -i 's/OpenWrt/Xiaomi-Router/g' package/base-files/files/bin/config_generate
#修改型号显示
sed -i 's/Xiaomi Redmi Router AC2100/Redmi AC2100/g' target/linux/ramips/dts/mt7621_xiaomi_redmi-router-ac2100.dts
sed -i 's/Xiaomi Mi Router AC2100/Xiaomi AC2100/g' target/linux/ramips/dts/mt7621_xiaomi_mi-router-ac2100.dts
#删除自带低版本xray-core
rm -rf feeds/packages/net/xray-core
rm -rf package/feeds/packages/xray-core
#复制uci-defaults脚本 
mkdir -p files/etc/uci-defaults
cp -f uci-scripts/* files/etc/uci-defaults
#复制内核5.10版本CPU超频补丁
#\cp -rf extra-files/322-mt7621-fix-cpu-clk-add-clkdev.patch target/linux/ramips/patches-5.10/322-mt7621-fix-cpu-clk-add-clkdev.patch
#设置WIFI
#sed -i 's/OpenWrt/coolxiaomi/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i 's/wireless.default_radio${devidx}.encryption=none/wireless.default_radio${devidx}.encryption=psk-mixed/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i '/encryption/a\set wireless.default_radio${devidx}.key=coolxiaomi' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#修改登录密码为coolxiaomi
#sed -i '/root/croot:$1$CBd7u73H$LvSDVXLBrzpk4JfuuN.Lv1:18676:0:99999:7:::' package/base-files/files/etc/shadow
#切换ramips内核到5.15
#sed -i '/KERNEL_PATCHVER/cKERNEL_PATCHVER:=5.15' target/linux/ramips/Makefile

#删除一些zzz中的脚本
sed -i '/DISTRIB_/d' package/default-settings/files/zzz-default-settings
sed -i '/footer.htm/d' package/default-settings/files/zzz-default-settings
sed -i '/admin_status/d' package/default-settings/files/zzz-default-settings
