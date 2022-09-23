#!/bin/sh

GEODIR="package/passwall-dependencies/v2ray-geodata"

wget -O v2ray-rules-dat.latest https://api.github.com/repos/Loyalsoldier/v2ray-rules-dat/releases/latest

LATEST_VER=$(jq -r .tag_name v2ray-rules-dat.latest)

wget https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geoip.dat.sha256sum
wget https://github.com/Loyalsoldier/v2ray-rules-dat/releases/download/$LATEST_VER/geosite.dat.sha256sum

GEOIP_HASH=$(sed -n '1p' geoip.dat.sha256sum | cut -d ' ' -f 1)
GEOSITE_HASH=$(sed -n '1p' geosite.dat.sha256sum | cut -d ' ' -f 1)

sed -i "/GEOIP_VER:=/cGEOIP_VER:=$LATEST_VER" $GEODIR/Makefile
sed -i "/GEOSITE_VER:=/cGEOSITE_VER:=$LATEST_VER" $GEODIR/Makefile

sed -i '/HASH:=/d' $GEODIR/Makefile
sed -i "/FILE:=\$(GEOIP_FILE)/a\  HASH:=$GEOIP_HASH" $GEODIR/Makefile
sed -i "/FILE:=\$(GEOSITE_FILE)/a\  HASH:=$GEOSITE_HASH" $GEODIR/Makefile

sed -i 's|v2fly/geoip|Loyalsoldier/v2ray-rules-dat|g' $GEODIR/Makefile
sed -i 's|v2fly/domain-list-community|Loyalsoldier/v2ray-rules-dat|g' $GEODIR/Makefile
sed -i 's|dlc.dat|geosite.dat|g' $GEODIR/Makefile

rm -f v2ray-rules-dat.latest geoip.dat.sha256sum geosite.dat.sha256sum
