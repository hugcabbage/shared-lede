#!/bin/sh

# download base code
CODE_DIR=_firmware_code
SWITCH_TAG_FLAG=false
git clone https://github.com/x-wrt/x-wrt.git $CODE_DIR
if $SWITCH_TAG_FLAG; then
    cd $CODE_DIR
    LATEST_TAG=$(git tag --sort=creatordate | awk 'END {print}')
    git checkout $LATEST_TAG
    echo "已切换到最近稳定版本$LATEST_TAG"
    cd ..
fi
mv ./$CODE_DIR/* ./

# download app codes
SUPPLY_DIR=_supply_packages
echo "src-link supply $PWD/$SUPPLY_DIR" >> feeds.conf.default
mkdir $SUPPLY_DIR && cd $SUPPLY_DIR
git clone --depth 1 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/yichya/luci-app-xray.git
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall-packages.git pw-dependencies
svn export https://github.com/xiaorouji/openwrt-passwall/trunk/luci-app-passwall
svn export https://github.com/xiaorouji/openwrt-passwall2/trunk/luci-app-passwall2
svn export https://github.com/vernesong/OpenClash/trunk/luci-app-openclash
