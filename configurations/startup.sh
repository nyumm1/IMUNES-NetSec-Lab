#!/bin/bash

# IMUNES-NetSec-Lab startup script!
# usage: sudo bash startup.sh :)

if [ "$EUID" -ne 0 ]; then
	echo "Start as root: sudo bash startup.sh"
	exit 1
fi

LABDIR="$(dirname "$0")"

echo "IMUNES-NetSec-Lab Startup!"

# DNS Server
echo "[1/3] DNS startup"
himage DNS-server mkdir -p /etc/bind/zones
hcp $LABDIR/DNS/named.conf.options DNS-server:/etc/bind/named.conf.options
hcp $LABDIR/DNS/named.conf.local DNS-server:/etc/bind/named.conf.local
hcp $LABDIR/DNS/Zones/db.office.lan DNS-server:/etc/bind/zones/db.office.lan
hcp $LABDIR/DNS/Zones/db.server DNS-server:/etc/bind/zones/db.server
hcp $LABDIR/DNS/Zones/db.finance DNS-server:/etc/bind/zones/db.finance
hcp $LABDIR/DNS/Zones/db.hr DNS-server:/etc/bind/zones/db.hr
hcp $LABDIR/DNS/Zones/db.it DNS-server:/etc/bind/zones/db.it
hcp $LABDIR/DNS/Zones/db.mgmt DNS-server:/etc/bind/zones/db.mgmt

himage DNS-server named -c /etc/bind/named.conf
echo "DNS Server started @10.0.10.11"

# Syslog server
echo "[2/3] Syslog server startup"
himage Syslog mkdir -p /var/log/remote
hcp $LABDIR/Syslog/rsyslog-server.conf Syslog:/tmp/rsyslog-server.conf
himage Syslog sh -c 'cat /tmp/rsyslog-server.conf >> /etc/rsyslog.conf'
himage Syslog rsyslogd
echo "Syslog server started @10.0.50.10"

echo "[3/3] Syslog clients startup"
NODES="MAIN-router Server-router FIN-router HR-router IT-router Mgmt-router \
	DNS-server DHCP-server File-server Web-server \
	HR-pc1 HR-pc2 HR-pc3 HR-pc4 \
	IT-pc1 IT-pc2 IT-pc3 IT-pc4 \
	FIN-pc1 FIN-pc2 FIN-pc3 MGMT-pc1"

for node in $NODES; do
	himage $node sh -c 'echo "*.* @10.0.50.10:514" >> /etc/rsyslog.conf'
	himage $node rsyslogd 2>/dev/null
done
echo "Syslog nodes working!"


echo " Lab ready!"
echo " DNS: 10.0.10.11"
echo " Syslog: 10.0.50.10"
