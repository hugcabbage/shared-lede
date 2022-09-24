#!/bin/sh
# 下载源码
git clone -b master --single-branch https://github.com/hugcabbage/openwrt
mv ./openwrt/* ./

# 下载插件
mkdir -p package/myapps
cd package/myapps
git clone https://github.com/jerrykuku/luci-theme-argon.git
git clone https://github.com/jerrykuku/luci-app-argon-config.git
git clone https://github.com/jerrykuku/luci-app-vssr.git
git clone https://github.com/jerrykuku/lua-maxminddb.git
git clone https://github.com/Ausaci/luci-app-nat6-helper.git
svn co https://github.com/vernesong/OpenClash/trunk/luci-app-openclash
git clone -b packages https://github.com/xiaorouji/openwrt-passwall.git passwall-dependencies
git clone -b luci https://github.com/xiaorouji/openwrt-passwall.git luci-app-passwall
git clone https://github.com/xiaorouji/openwrt-passwall2.git
svn co https://github.com/linkease/nas-packages-luci/trunk/luci/luci-app-ddnsto
