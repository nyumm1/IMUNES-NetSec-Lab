Journal

19/05/2026
Start of this whole setup, I feel like the amount of things that need to be done require a dedicated journal to keep track!
For now, I have configured a DHCP server using the office_dhcp.conf file that can be made to work, but unfortunately I cannot get the department routers to act like relays of the DHCP server so for now I will keep static addresses with a DHCP server here in case I want to make a DHCP specific attack (Rogue DHCP for example)

21/05/2026
Finished up the DHCP Test folder with a working test, next up will be DNS where I think the best would be to first do Test file then the config for the whole office... Definitely will have to revisit DHCP office setup as I see the intended way to use it is different from the one I ended up using. Updated the README.md and added the current topology as well as the current .imn file.

23/05/2026
Managed to get DNS to work on the full topology, tried again to setup a network wide DHCP but again to no awail. Changed the routing protocol to OSPF and started using frr instead of quagga for routers but I still think that in general it doesn't really change a whole lot. Didn't really have the time to upload all of the changes, but my current priority would be to upload a DNS test and then based on that refine the currently Claude generated DNS config on the whole office network to something I made myself.
