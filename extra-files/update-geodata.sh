#!/usr/bin/env bash

echo "Start to update geodata..."
GEOMK=package/feeds/packages/v2ray-geodata/Makefile
[ -e "$GEOMK" ] || GEOMK=package/feeds/supply/v2ray-geodata/Makefile
[ -e "$GEOMK" ] || exit 1

LATEST_VER=$(curl -fs https://api.github.com/repos/Loyalsoldier/v2ray-rules-dat/releases/latest | jq -r .'tag_name')
MARK="# The file has been modified by@hugcabbage $LATEST_VER"
if grep -q "$MARK" $GEOMK; then
    echo "geodata is newest"
    exit 0
else
    sed -i "1i $MARK" $GEOMK
fi

GEOIP_HASH=$(curl -fsL https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geoip.dat.sha256sum | awk '{print $1}')
GEOSITE_HASH=$(curl -fsL https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geosite.dat.sha256sum | awk '{print $1}')

sed -i "/GEOIP_VER:=/cGEOIP_VER:=$LATEST_VER" $GEOMK
sed -i "/GEOSITE_VER:=/cGEOSITE_VER:=$LATEST_VER" $GEOMK

sed -i '/HASH:=/d' $GEOMK
sed -i "/FILE:=\$(GEOIP_FILE)/a\  HASH:=$GEOIP_HASH" $GEOMK
sed -i "/FILE:=\$(GEOSITE_FILE)/a\  HASH:=$GEOSITE_HASH" $GEOMK

sed -i 's|v2fly/geoip|Loyalsoldier/v2ray-rules-dat|g' $GEOMK
sed -i 's|v2fly/domain-list-community|Loyalsoldier/v2ray-rules-dat|g' $GEOMK
sed -i 's|dlc.dat|geosite.dat|g' $GEOMK

echo "Updating geodata done"
