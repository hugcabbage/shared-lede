#设置ipv6解析
uci set network.globals.ula_prefix=2fff:1:1::/64
uci commit network
uci set dhcp.@dnsmasq[0].filter_aaaa=0
uci commit dhcp
