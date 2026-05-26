Journal

19/05/2026
Start of this whole setup, I feel like the amount of things that need to be done require a dedicated journal to keep track!
For now, I have configured a DHCP server using the office_dhcp.conf file that can be made to work, but unfortunately I cannot get the department routers to act like relays of the DHCP server so for now I will keep static addresses with a DHCP server here in case I want to make a DHCP specific attack (Rogue DHCP for example)

21/05/2026
Finished up the DHCP Test folder with a working test, next up will be DNS where I think the best would be to first do Test file then the config for the whole office... Definitely will have to revisit DHCP office setup as I see the intended way to use it is different from the one I ended up using. Updated the README.md and added the current topology as well as the current .imn file.

23/05/2026
Managed to get DNS to work on the full topology, tried again to setup a network wide DHCP but again to no awail. Changed the routing protocol to OSPF and started using frr instead of quagga for routers but I still think that in general it doesn't really change a whole lot. Didn't really have the time to upload all of the changes, but my current priority would be to upload a DNS test and then based on that refine the currently Claude generated DNS config on the whole office network to something I made myself.

25/05/2026
Got DNSTest to work and actually learned a lot about how to configure DNS! Next challenge is the same as the one labeled before: refine the current DNS config of the office myself :)

26/06/2026
Loads of things done today, so let's go through it one by one! Firstly, made my own DNS configuration for the office topology and tested it out (first try btw :P) and it was uploaded in the configurations/DNS folder with all of the zones and conf files! Secondly, I managed to setup the Syslog server to work, although I'm not too happy with the results as I think I haven't really configured it as I initially wished (probably am missing per device configs as individual logs aren't seen outside the mgmt subnet, but the DNS server is sending it's logs very nicely :D. Thirdly, I made a startup shell script as I have no intention of typing sudo hcp blah blah 10 times every time I want to test DNS... The script works fine, but an important part is the way all of the files are organised so I also uploaded my own tree of the Office-Lab folder so that anyone can replicate it if necessarry! Fourthly, I made some slight adjustments to the topology (mainly just names) and uploaded a new imn file and a new png file!
