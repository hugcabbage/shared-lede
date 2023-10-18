#!/bin/sh

# download base code
CODE_DIR=_firmware_code
git clone --depth 1 -b main https://github.com/Lienol/openwrt $CODE_DIR
mv ./$CODE_DIR/* ./

# download app codes
mkdir -p package/_supply_packages && cd package/_supply_packages
git clone --depth 1 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-vssr.git
git clone --depth 1 https://github.com/jerrykuku/lua-maxminddb.git
git clone --depth 1 https://github.com/Ausaci/luci-app-nat6-helper.git
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall-packages.git pw-dependencies
svn export https://github.com/xiaorouji/openwrt-passwall/trunk/luci-app-passwall
svn export https://github.com/xiaorouji/openwrt-passwall2/trunk/luci-app-passwall2
svn export https://github.com/vernesong/OpenClash/trunk/luci-app-openclash
