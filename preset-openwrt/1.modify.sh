#!/usr/bin/env bash

# modify login IP
#sed -i 's/192.168.1.1/192.168.10.1/g' package/base-files/files/bin/config_generate

# copy uci-defaults script(s)
mkdir -p files/etc/uci-defaults
cp $(dirname $0)/uci-scripts/* files/etc/uci-defaults/

# modify default package(s)
if ! grep -q "dnsmasq-full" include/target.mk; then
    sed -i 's/dnsmasq/dnsmasq-full/g' include/target.mk
fi

# modify luci-app-xray category
modify_lax_category() {
    local mk=$1
    [ -e $mk ] || return
    sed -i 's/SECTION:=Custom/CATEGORY:=LuCI/g' $mk
    sed -i 's/CATEGORY:=Extra packages/SUBMENU:=3. Applications/g' $mk
}
modify_lax_category 'package/feeds/supply/luci-app-xray-core/Makefile'
modify_lax_category 'package/feeds/supply/luci-app-xray-status/Makefile'

# replace geodata source
. $(dirname $0)/../extra-files/update-geodata.sh
