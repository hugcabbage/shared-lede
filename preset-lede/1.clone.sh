#!/bin/sh

# download base code
CODE_DIR=_firmware_code
git clone --depth 1 https://github.com/coolsnowwolf/lede.git $CODE_DIR
mv ./$CODE_DIR/* ./

# download app codes
rm -rf package/lean/luci-theme-argon
mkdir -p package/_supply_packages && cd package/_supply_packages
git clone --depth 1 -b 18.06 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/kenzok8/openwrt-packages.git
git clone --depth 1 https://github.com/kenzok8/small.git
git clone --depth 1 https://github.com/Ausaci/luci-app-nat6-helper.git
