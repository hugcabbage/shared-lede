#!/bin/sh

AIMFILE=target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-3g-v2.dtsi
AIDFILE=target/linux/ramips/dts/mt7621_youhua_wr1200js.dts

SPECIFIC_LINE=$(sed -n '/&spi0/=' $AIMFILE)
BASE_TEXT=$(sed '/&spi0/,/^};/d' $AIMFILE)

echo "$BASE_TEXT" | sed -n "1,${SPECIFIC_LINE}p" > $AIMFILE
sed -n '/&spi0/,/^};/p' $AIDFILE >> $AIMFILE
echo "$BASE_TEXT" | sed -n "$SPECIFIC_LINE,\$p" >> $AIMFILE
sed -i "${SPECIFIC_LINE}d" $AIMFILE

MT7621MK=target/linux/ramips/image/mt7621.mk

sed -i '/Device\/xiaomi_mi-router-4a-gigabit/,/Mi Router 4A/ s/14848k/16064k/' $MT7621MK
sed -i '/Device\/xiaomi_mi-router-3g-v2/,/mir3g-v2/ s/14848k/16064k/' $MT7621MK
