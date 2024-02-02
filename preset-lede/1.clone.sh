#!/usr/bin/env bash

# download base code
CODE_DIR=_firmware_code
git clone --depth 1 https://github.com/coolsnowwolf/lede.git $CODE_DIR
mv ./$CODE_DIR/* ./

# download app codes
SUPPLY_DIR=_supply_packages
echo "src-link supply $PWD/$SUPPLY_DIR" >> feeds.conf.default
mkdir $SUPPLY_DIR && cd $SUPPLY_DIR
git clone --depth 1 https://github.com/kenzok8/openwrt-packages.git
git clone --depth 1 https://github.com/kenzok8/small.git
git clone --depth 1 https://github.com/Ausaci/luci-app-nat6-helper.git
