#!/usr/bin/env bash
# Use for testing in local environment
# Run this script in a blank directory

STDIR=$(dirname $(realpath $0))
. $STDIR/tools/color.sh

# download base code
echo "Start to download the base code..."

CODE_DIR=$PWD/${1:-_test_code}
CODE_URL=https://git.openwrt.org/openwrt/openwrt.git
CODE_BRANCH=openwrt-23.05
SWITCH_LATEST_TAG=false

if [ -d "$CODE_DIR" ]; then
    echo "Updating base code from $(cyan $CODE_URL@$CODE_BRANCH)"
    cd $CODE_DIR
    git pull
    cd - > /dev/null
else
    echo "Cloning base code from $(cyan $CODE_URL@$CODE_BRANCH)"
    git clone --single-branch -b $CODE_BRANCH $CODE_URL $CODE_DIR
fi

if $SWITCH_LATEST_TAG; then
    cd $CODE_DIR
    LATEST_TAG_HASH=$(git rev-list --tags --max-count=1)
    if [ -z "$LATEST_TAG_HASH" ]; then
        red "No tag to switch, keep the latest commit"
    else
        git checkout $LATEST_TAG_HASH
        LATEST_TAG=$(git describe --tags $LATEST_TAG_HASH)
        green "The code has been switched to the latest stable version $LATEST_TAG"
    fi
    cd - > /dev/null
fi

cd $CODE_DIR

# download app codes
echo "Start to download app codes..."

SUPPLY_DIR=$PWD/_supply_packages
bdir=$PWD/._b_supply_packages

if ! grep -q "src-link supply $SUPPLY_DIR" feeds.conf.default; then
    echo "src-link supply $SUPPLY_DIR" >> feeds.conf.default
fi
mkdir -p $SUPPLY_DIR
cd $SUPPLY_DIR

declare -A REPOS=(
     ["https://github.com/jerrykuku/luci-theme-argon.git"]=""
     ["https://github.com/jerrykuku/luci-app-argon-config.git"]=""
     ["https://github.com/sbwml/luci-app-alist.git"]=""
     ["https://github.com/yichya/luci-app-xray.git"]=":$bdir/luci-app-xray"
     ["https://github.com/xiaorouji/openwrt-passwall-packages.git"]=":pw-dependencies"
     ["https://github.com/xiaorouji/openwrt-passwall.git"]=":$bdir/openwrt-passwall"
     ["https://github.com/xiaorouji/openwrt-passwall2.git"]=":$bdir/openwrt-passwall2"
     ["https://github.com/vernesong/OpenClash.git"]=":$bdir/openclash"
)

for REPO_URL in "${!REPOS[@]}"; do
    IFS=":" read -r BRANCH LOCAL_PATH <<< "${REPOS[$REPO_URL]}"
    REPO_NAME=$(basename "$REPO_URL" .git)
    LOCAL_PATH=${LOCAL_PATH:-$REPO_NAME}

    if [ -d "$LOCAL_PATH" ]; then
        echo "Updating $REPO_NAME from $(cyan $REPO_URL)"
        cd $LOCAL_PATH
        git pull
        cd - > /dev/null
    else
        if [ -z "$BRANCH" ]; then
            echo "Cloning code from $(cyan $REPO_URL)"
            git clone --depth 1 $REPO_URL $LOCAL_PATH
        else
            echo "Cloning code from $(cyan $REPO_URL@$BRANCH)"
            git clone -b $BRANCH --depth 1 $REPO_URL $LOCAL_PATH
        fi
    fi
done

rsync -a --delete $bdir/luci-app-xray/core/ luci-app-xray-core/
rsync -a --delete $bdir/luci-app-xray/status/ luci-app-xray-status/
rsync -a --delete $bdir/openwrt-passwall/luci-app-passwall/ luci-app-passwall/
rsync -a --delete $bdir/openwrt-passwall2/luci-app-passwall2/ luci-app-passwall2/
rsync -a --delete $bdir/openclash/luci-app-openclash/ luci-app-openclash/

cd $CODE_DIR

./scripts/feeds update -a
./scripts/feeds install -a

$STDIR/../preset-openwrt/1.modify.sh
