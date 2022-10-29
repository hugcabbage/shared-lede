#!/bin/sh

# 下载源码
git clone --depth 1 -b master https://github.com/Lienol/openwrt openwrt && mv ./openwrt/* ./

# 下载插件
mkdir -p package/supply-packages && cd package/supply-packages
git clone --depth 1 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-vssr.git
git clone --depth 1 https://github.com/jerrykuku/lua-maxminddb.git
git clone --depth 1 https://github.com/Ausaci/luci-app-nat6-helper.git
git clone --depth 1 -b packages https://github.com/xiaorouji/openwrt-passwall.git pw-dependencies
svn export https://github.com/xiaorouji/openwrt-passwall/branches/luci/luci-app-passwall
svn export https://github.com/xiaorouji/openwrt-passwall2/trunk/luci-app-passwall2
svn export https://github.com/vernesong/OpenClash/trunk/luci-app-openclash
