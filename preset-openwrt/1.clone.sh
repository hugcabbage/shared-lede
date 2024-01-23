#!/usr/bin/env bash

# download base code
CODE_DIR=_firmware_code
CODE_URL=https://git.openwrt.org/openwrt/openwrt.git
CODE_BRANCH=openwrt-23.05
SWITCH_LATEST_TAG=false
git clone --single-branch -b $CODE_BRANCH $CODE_URL $CODE_DIR
if $SWITCH_LATEST_TAG; then
    cd $CODE_DIR
    LATEST_TAG_HASH=$(git rev-list --tags --max-count=1)
    if [ -z "$LATEST_TAG_HASH" ]; then
        echo "No tag to switch, keep the latest commit"
    else
        git checkout $LATEST_TAG_HASH
        LATEST_TAG=$(git describe --tags $LATEST_TAG_HASH)
        echo "The code has been switched to the latest stable version $LATEST_TAG"
    fi
    cd ..
fi
mv ./$CODE_DIR/* ./

# download app codes
SUPPLY_DIR=_supply_packages
echo "src-link supply $PWD/$SUPPLY_DIR" >> feeds.conf.default
mkdir $SUPPLY_DIR && cd $SUPPLY_DIR
git clone --depth 1 https://github.com/jerrykuku/luci-theme-argon.git
git clone --depth 1 https://github.com/jerrykuku/luci-app-argon-config.git
git clone --depth 1 https://github.com/sbwml/luci-app-alist.git
git clone --depth 1 https://github.com/yichya/luci-app-xray.git && mv luci-app-xray/core luci-app-xray-core && mv luci-app-xray/status luci-app-xray-status && rm -rf luci-app-xray
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall-packages.git pw-dependencies
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall.git && mv openwrt-passwall/luci-app-passwall ./ && rm -rf openwrt-passwall
git clone --depth 1 https://github.com/xiaorouji/openwrt-passwall2.git && mv openwrt-passwall2/luci-app-passwall2 ./ && rm -rf openwrt-passwall2
git clone --depth 1 https://github.com/vernesong/OpenClash.git && mv OpenClash/luci-app-openclash ./ && rm -rf OpenClash
