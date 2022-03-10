#!/bin/sh
# 下载源码
git clone -b main --single-branch https://github.com/Lienol/openwrt
mv ./openwrt/* ./

# 下载自定义插件
cd package
git clone https://github.com/jerrykuku/luci-theme-argon.git
git clone https://github.com/jerrykuku/luci-app-argon-config.git
git clone https://github.com/Ausaci/luci-app-nat6-helper.git
git clone -b packages --single-branch https://github.com/xiaorouji/openwrt-passwall.git
git clone -b luci --single-branch https://github.com/xiaorouji/openwrt-passwall.git luci-app-passwall
