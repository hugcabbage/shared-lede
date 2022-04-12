#!/bin/sh
#修改登录IP
sed -i 's/192.168.1.1/192.168.31.1/g' package/base-files/files/bin/config_generate
#修改主机名
sed -i 's/OpenWrt/Xiaomi-Router/g' package/base-files/files/bin/config_generate
#修改型号显示
sed -i 's/Xiaomi Mi Router 4A Gigabit Edition/Xiaomi 4A Gigabit/g' target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-gigabit.dts
sed -i 's/Xiaomi Mi Router 3G v2/Xiaomi 3G v2/g' target/linux/ramips/dts/mt7621_xiaomi_mi-router-3g-v2.dts
#修改固件大小、复制闪存布局文件
sed -i '/Device\/xiaomi_mi-router-4a-gigabit/,/Mi Router 4A/ s/14848k/16064k/' target/linux/ramips/image/mt7621.mk
sed -i '/Device\/xiaomi_mi-router-3g-v2/,/mir3g-v2/ s/14848k/16064k/' target/linux/ramips/image/mt7621.mk
\cp -rf extra_files/mt7621_xiaomi_mi-router-4a-3g-v2.dtsi target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-3g-v2.dtsi
#配置smartdns、ipv6、主题、vssr 
sed -i '/exit 0/d' package/lean/default-settings/files/zzz-default-settings
#cat default-settings/config_smartdns >> package/lean/default-settings/files/zzz-default-settings
cat default-settings/config_ipv6 >> package/lean/default-settings/files/zzz-default-settings
cat default-settings/config_theme >> package/lean/default-settings/files/zzz-default-settings
#cat default-settings/config_vssr >> package/lean/default-settings/files/zzz-default-settings
echo "exit 0" >> package/lean/default-settings/files/zzz-default-settings
#切换ramips内核到5.10
sed -i '/KERNEL_PATCHVER/cKERNEL_PATCHVER:=5.10' target/linux/ramips/Makefile
#复制内核5.10版本CPU超频补丁
#\cp -rf extra_files/322-mt7621-fix-cpu-clk-add-clkdev.patch target/linux/ramips/patches-5.10/322-mt7621-fix-cpu-clk-add-clkdev.patch
#设置WIFI
#sed -i 's/OpenWrt/coolxiaomi/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i 's/wireless.default_radio${devidx}.encryption=none/wireless.default_radio${devidx}.encryption=psk-mixed/g' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#sed -i '/encryption/a\set wireless.default_radio${devidx}.key=coolxiaomi' package/kernel/mac80211/files/lib/wifi/mac80211.sh
#修改登录密码为coolxiaomi
#sed -i '/root/croot:$1$CBd7u73H$LvSDVXLBrzpk4JfuuN.Lv1:18676:0:99999:7:::' package/base-files/files/etc/shadow
#切换ramips内核到5.15
#sed -i '/KERNEL_PATCHVER/cKERNEL_PATCHVER:=5.15' target/linux/ramips/Makefile
