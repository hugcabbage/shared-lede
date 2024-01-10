#!/bin/sh

[ -z "$GEODIR" ] && GEODIR=package/_supply_packages/pw-dependencies/v2ray-geodata

LATEST_VER=$(curl -fs https://api.github.com/repos/Loyalsoldier/v2ray-rules-dat/releases/latest | jq -r .'tag_name')

GEOIP_HASH=$(curl -fsL https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geoip.dat.sha256sum | awk '{print $1}')

GEOSITE_HASH=$(curl -fsL https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geosite.dat.sha256sum | awk '{print $1}')

sed -i "/GEOIP_VER:=/cGEOIP_VER:=$LATEST_VER" $GEODIR/Makefile
sed -i "/GEOSITE_VER:=/cGEOSITE_VER:=$LATEST_VER" $GEODIR/Makefile

sed -i '/HASH:=/d' $GEODIR/Makefile
sed -i "/FILE:=\$(GEOIP_FILE)/a\  HASH:=$GEOIP_HASH" $GEODIR/Makefile
sed -i "/FILE:=\$(GEOSITE_FILE)/a\  HASH:=$GEOSITE_HASH" $GEODIR/Makefile

sed -i 's|v2fly/geoip|Loyalsoldier/v2ray-rules-dat|g' $GEODIR/Makefile
sed -i 's|v2fly/domain-list-community|Loyalsoldier/v2ray-rules-dat|g' $GEODIR/Makefile
sed -i 's|dlc.dat|geosite.dat|g' $GEODIR/Makefile
