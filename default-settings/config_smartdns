#增加smartdns上游服务器
rm -rf /etc/config/smartdns
touch /etc/config/smartdns
echo "config smartdns" >> /etc/config/smartdns
echo "	option server_name 'smartdns'" >> /etc/config/smartdns
echo "	option tcp_server '1'" >> /etc/config/smartdns
echo "	option ipv6_server '1'" >> /etc/config/smartdns
echo "	option serve_expired '0'" >> /etc/config/smartdns
echo "	option rr_ttl_min '300'" >> /etc/config/smartdns
echo "	option seconddns_tcp_server '1'" >> /etc/config/smartdns
echo "	option seconddns_no_rule_addr '0'" >> /etc/config/smartdns
echo "	option seconddns_no_rule_nameserver '0'" >> /etc/config/smartdns
echo "	option seconddns_no_rule_ipset '0'" >> /etc/config/smartdns
echo "	option coredump '0'" >> /etc/config/smartdns
echo "	option dualstack_ip_selection '0'" >> /etc/config/smartdns
echo "	option port '6053'" >> /etc/config/smartdns
echo "	option cache_size '2048'" >> /etc/config/smartdns
echo "	option seconddns_enabled '1'" >> /etc/config/smartdns
echo "	option seconddns_server_group 'abroad'" >> /etc/config/smartdns
echo "	option force_aaaa_soa '0'" >> /etc/config/smartdns
echo "	option seconddns_port '5335'" >> /etc/config/smartdns
echo "	option enabled '0'" >> /etc/config/smartdns
echo "	option redirect 'none'" >> /etc/config/smartdns
echo "	option seconddns_no_speed_check '1'" >> /etc/config/smartdns
echo "	option seconddns_no_rule_soa '0'" >> /etc/config/smartdns
echo "	option seconddns_no_dualstack_selection '1'" >> /etc/config/smartdns
echo "	option seconddns_no_cache '1'" >> /etc/config/smartdns
echo "	option prefetch_domain '1'" >> /etc/config/smartdns
echo "	list old_redirect 'none'" >> /etc/config/smartdns
echo "	list old_port '6053'" >> /etc/config/smartdns
echo "	list old_enabled '1'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option blacklist_ip '0'" >> /etc/config/smartdns
echo "	option port '853'" >> /etc/config/smartdns
echo "	option server_group 'abroad'" >> /etc/config/smartdns
echo "	option type 'tls'" >> /etc/config/smartdns
echo "	option ip 'dns.google'" >> /etc/config/smartdns
echo "	option name '谷歌DNS'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option ip '1.1.1.1'" >> /etc/config/smartdns
echo "	option port '853'" >> /etc/config/smartdns
echo "	option type 'tls'" >> /etc/config/smartdns
echo "	option name 'Cloudflare DNS'" >> /etc/config/smartdns
echo "	option server_group 'abroad'" >> /etc/config/smartdns
echo "	option blacklist_ip '0'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option ip '114.114.114.114'" >> /etc/config/smartdns
echo "	option port '53'" >> /etc/config/smartdns
echo "	option type 'udp'" >> /etc/config/smartdns
echo "	option name '114DNS'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option type 'udp'" >> /etc/config/smartdns
echo "	option port '53'" >> /etc/config/smartdns
echo "	option ip '223.5.5.5'" >> /etc/config/smartdns
echo "	option name '阿里DNS'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option type 'udp'" >> /etc/config/smartdns
echo "	option port '53'" >> /etc/config/smartdns
echo "	option name '阿里DNS'" >> /etc/config/smartdns
echo "	option ip '223.6.6.6'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option type 'udp'" >> /etc/config/smartdns
echo "	option ip '1.2.4.8'" >> /etc/config/smartdns
echo "	option port '53'" >> /etc/config/smartdns
echo "	option name 'CNNIC DNS'" >> /etc/config/smartdns
echo "config server" >> /etc/config/smartdns
echo "	option enabled '1'" >> /etc/config/smartdns
echo "	option type 'udp'" >> /etc/config/smartdns
echo "	option ip '210.2.4.8'" >> /etc/config/smartdns
echo "	option port '53'" >> /etc/config/smartdns
echo "	option name 'CNNIC DNS'" >> /etc/config/smartdns

#增加smartdns address netflix列表，禁止ipv6返回
echo "address /fast.com/#6" >> /etc/smartdns/address.conf
echo "address /netflix.ca/#6" >> /etc/smartdns/address.conf
echo "address /netflix.com/#6" >> /etc/smartdns/address.conf
echo "address /netflix.net/#6" >> /etc/smartdns/address.conf
echo "address /netflixinvestor.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixtechblog.com/#6" >> /etc/smartdns/address.conf
echo "address /nflxext.com/#6" >> /etc/smartdns/address.conf
echo "address /nflximg.com/#6" >> /etc/smartdns/address.conf
echo "address /nflximg.net/#6" >> /etc/smartdns/address.conf
echo "address /nflxsearch.net/#6" >> /etc/smartdns/address.conf
echo "address /nflxso.net/#6" >> /etc/smartdns/address.conf
echo "address /nflxvideo.net/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest0.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest1.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest2.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest3.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest4.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest5.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest6.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest7.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest8.com/#6" >> /etc/smartdns/address.conf
echo "address /netflixdnstest9.com/#6" >> /etc/smartdns/address.conf
