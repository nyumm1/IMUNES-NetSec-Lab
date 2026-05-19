DHCP

DHCP server configuration file with static addresses for the MGMT space as I wanted both the Attacker (MGMT-pc1) and the logging server to have static addresses.
Other than that, it is a normal dhcp config where we configure the subnets for the departments.

USAGE:
First you have to copy the file office_dhcp.conf to the DHCP-server using the terminal of the VM instead of the DHCP-server VM
Command:
hcp office_dhcp.conf DHCP-server:/etc/dhcp/dhcpd.conf

This way you have updated the config file for DHCP.
After this, the next step is to change the file isc-dhcp-server with the given interface for IPv4 as that way when starting only the DHCPv4 will start.
Command:
nano /etc/default/isc-dhcp-server
INTERFACESv4=""   <--find this and change to:
INTERFACESv4="eth0"

now we can start the isc-dhcp-server service using:
Command:
service isc-dhcp-server restart

Now it should be up and running, but it will only do DHCP inside of the SRV subnet, but as all of the connected devices inside the SRV subnet have static addresses, nothing will really happen.

What is missing here for DHCP to work is to setup all of the routers as isc-dhcp-relays where you can then "extend the area" of DHCP to their subnets aswell... I currently have not found a way to do this as it is not natively installed on the routers and there seems to be no internet connection even when using ext as the external conncetion to the internet.

It's still here in the case that we need a DHCP server for DHCP focused attacks such as Rogue DHCP (setting up a malicious DHCP server that takes over the work of the real server) and DHCP starvation (flooding the DHCP server with fake requests to empty out the address pool)
