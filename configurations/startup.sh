#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "Start as root: sudo bash startup.sh"
	exit 1
fi

LABDIR="$(dirname "$0")"

echo "IMUNES-NetSec-Lab Startup!"

# Internet connection
echo "[0/4] Trying to establish a network connection"


EXT_IP=$(ip addr show enp0s1 2>/dev/null | grep "inet " | awk '{print $2}')
GW=$(ip route show dev enp0s1 2>/dev/null | grep default | awk '{print $3}')

if [ -n "$EXT_IP" ] && [ -n "$GW" ]; then
	MAIN_IP=$(echo $EXT_IP | sed 's/\.[0-9]*\//.100\//')
	echo "Internet available: $EXT_IP ext via $GW"
	echo "MAIN-router eth0: $MAIN_IP"
	INTERNET=true
else
	echo "Offline mode"
	INTERNET=false
fi

echo "Start the office_top.imn experiment and press Enter when the experiment is live"
read


# DNS Server
echo "[1/4] DNS startup"
himage DNS-server mkdir -p /etc/bind/zones
hcp $LABDIR/DNS/named.conf.options DNS-server:/etc/bind/named.conf.options
hcp $LABDIR/DNS/named.conf.local DNS-server:/etc/bind/named.conf.local
hcp $LABDIR/DNS/Zones/db.office.lan DNS-server:/etc/bind/zones/db.office.lan
hcp $LABDIR/DNS/Zones/db.server DNS-server:/etc/bind/zones/db.server
hcp $LABDIR/DNS/Zones/db.finance DNS-server:/etc/bind/zones/db.finance
hcp $LABDIR/DNS/Zones/db.hr DNS-server:/etc/bind/zones/db.hr
hcp $LABDIR/DNS/Zones/db.it DNS-server:/etc/bind/zones/db.it
hcp $LABDIR/DNS/Zones/db.mgmt DNS-server:/etc/bind/zones/db.mgmt

if [ "$INTERNET" = true ]; then
	himage DNS-server sh -c "sed -i 's/forwarders { };/forwarders { $GW; };/' /etc/bind/named.conf.options"
	himage DNS-server sh -c "sed -i 's/recursion no/recursion yes/' /etc/bind/named.conf.options"
fi

himage DNS-server named -c /etc/bind/named.conf
echo "DNS Server started @10.0.10.11"

# Syslog server
echo "[2/4] Syslog server startup"
himage Syslog mkdir -p /var/log/remote
hcp $LABDIR/Syslog/rsyslog-server.conf Syslog:/tmp/rsyslog-server.conf
himage Syslog sh -c 'cat /tmp/rsyslog-server.conf >> /etc/rsyslog.conf'
himage Syslog rsyslogd
echo "Syslog server started @10.0.50.10"

echo "[3/4] Syslog clients startup"
NODES="MAIN-router Server-router FIN-router HR-router IT-router Mgmt-router \
	DNS-server DHCP-server File-server Web-server \
	HR-pc1 HR-pc2 HR-pc3 HR-pc4 \
	IT-pc1 IT-pc2 IT-pc3 IT-pc4 \
	FIN-pc1 FIN-pc2 FIN-pc3 MGMT-pc1"

for node in $NODES; do
	himage $node sh -c 'echo "nameserver 10.0.10.11" > /etc/resolv.conf'
	himage $node sh -c 'echo "search office.lan" >> /etc/resolv.conf'
	if [ "$INTERNET" = true ]; then
		himage $node sh -c 'echo "nameserver 8.8.8.8" >> /etc/resolv.conf'
	fi
	himage $node sh -c 'echo "*.* @10.0.50.10:514" >> /etc/rsyslog.conf'
	himage $node rsyslogd 2>/dev/null
done
echo "Syslog nodes working!"

echo "[4/4] Configuring network access"
if [ "$INTERNET" = true ]; then
	himage MAIN-router ip addr flush dev eth0
	himage MAIN-router ip addr add $MAIN_IP dev eth0
	himage MAIN-router ip route add default via $GW
	himage MAIN-router iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
	himage MAIN-router sysctl -w net.ipv4.ip_forward=1

	himage MAIN-router vtysh -c "configure terminal" \
				 -c "router ospf" \
				 -c "default-information originate always" \
				 -c "exit" -c "exit" -c "write memory"

	echo "Network is active, gateway: $GW"
else
	echo "Internet not available, using local DNS"
fi


echo " Lab ready!"
echo " Internet: $INTERNET"
echo " DNS: 10.0.10.11"
echo " Syslog: 10.0.50.10"
