# Testing out the configuration of DHCP 
> Based on the laboratory textbook for Communication Networks class.

Steps necessary for creating and using the DHCP Server inside of IMUNES:

## Step 1: Create the dhcpd.conf file
The file can be seen in the folder. Won't be explaining it too much as most of it is standard...
Most important questions to be asked here are:
- What is the given subnet and what are the available addresses?
- Do some parts of the network have the need for static addresses?
- What is the router for the subnet?
- What file and where will be handling the leases?
- (When also having DNS configured) How will it interract with the DNS Server?
- Other default settings (will anyways be googled to see what is necessary)...

## Step 2: Transfer the files and startup the DHCP client
From my experience it should go something like this:
- Step 2.1: (VM terminal): hcp dhcpd.conf <DHCPServerName>:/<location_you_want> // transfer the config file to the DHCP server
- Step 2.2: (DHCPserver terminal): touch <location of .leases file> // if not already created, create the .leases address that is configured in Step 1
- Step 2.3: (DHCPserver terminal): dhcpd -cf /<path_to_dhcpd.conf>/dhcpd.conf // starts up DHCP on the DHCP server
- Step 2.4: (NetworkClient terminal -> example PC2): dhclient <interface_on_the_subnet> // let the DHCP host give you an IP address from the available subnet
- Step 2.STOP: (DHCPserver terminal): killall -9 dhcpd // closes DHCP on the DHCP server

This did in fact work and now is ready to be implemented on the larger office network... 
Still the same question remains about the relays but I might have to change up the strategy :)
