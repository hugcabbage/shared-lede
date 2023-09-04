#!/bin/sh

AIMFILE=target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-common.dtsi
AIDFILE=target/linux/ramips/dts/mt7621_youhua_wr1200js.dts
[ ! -e "$AIMFILE" ] && AIMFILE=target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-3g-v2.dtsi

SPECIFIC_LINE=$(sed -n '/&spi0/=' $AIMFILE)
BASE_TEXT=$(sed '/&spi0/,/^};/d' $AIMFILE)

echo "$BASE_TEXT" | sed -n "1,${SPECIFIC_LINE}p" > $AIMFILE
sed -n '/&spi0/,/^};/p' $AIDFILE >> $AIMFILE
echo "$BASE_TEXT" | sed -n "$SPECIFIC_LINE,\$p" >> $AIMFILE
sed -i "${SPECIFIC_LINE}d" $AIMFILE

EXFILE=target/linux/ramips/dts/mt7621_xiaomi_mi-router-4a-gigabit-v2.dts
MT7621MK=target/linux/ramips/image/mt7621.mk

if [ -e "$EXFILE" ]; then
    sed -i 's/partition@180000/partition@50000/' $EXFILE
    sed -i 's/0x180000 0xe70000/0x50000 0xfa0000/' $EXFILE
    sed -i 's/partitions {/partitions: partitions {/' $AIMFILE
    sed -i '/Device\/xiaomi_mi-router-4a-gigabit-v2/,/Mi Router 4A/ s/14784k/16000k/' $MT7621MK
fi

sed -i '/Device\/xiaomi_mi-router-4a-gigabit/,/Mi Router 4A/ s/14848k/16064k/' $MT7621MK
sed -i '/Device\/xiaomi_mi-router-3g-v2/,/Mi Router 3G/ s/14848k/16064k/' $MT7621MK
