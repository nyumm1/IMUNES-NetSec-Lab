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

26/05/2026
Loads of things done today, so let's go through it one by one! Firstly, made my own DNS configuration for the office topology and tested it out (first try btw :P) and it was uploaded in the configurations/DNS folder with all of the zones and conf files! Secondly, I managed to setup the Syslog server to work, although I'm not too happy with the results as I think I haven't really configured it as I initially wished (probably am missing per device configs as individual logs aren't seen outside the mgmt subnet, but the DNS server is sending it's logs very nicely :D. Thirdly, I made a startup shell script as I have no intention of typing sudo hcp blah blah 10 times every time I want to test DNS... The script works fine, but an important part is the way all of the files are organised so I also uploaded my own tree of the Office-Lab folder so that anyone can replicate it if necessarry! Fourthly, I made some slight adjustments to the topology (mainly just names) and uploaded a new imn file and a new png file!

28/05/2026 (typed and uploaded on 29th my bad)
Finally got the Office network connected to the internet!! Using the enp0s1 interface from my UTM virtual machine as a "stolen interface," it can now connect to anything on the internet. Alongside this, I have managed to setup the DNS server so that it has 8.8.8.8 (Google public DNS server) set as the forwarder so I can do dig @10.0.10.11 google.com and still get a good answer :)) Many changes to the startup.sh script as I had to take into account that getting the external IP address, gateway and corresponding IP for eth0 on the MAIN-router have to be done before the experiment starts (as it gets stolen once the experiment is up and running). I'm still not too happy about the script, as the default IP address given to eth0 on the MAIN-router can happen to be the address of another already working device which is not great but okay. This whole thing took a lot more work than expected as eduroam was not kind to my testing of this, and as I wanted to finally get firefox and sylpheed installed so I actually have access to all of the tools on imunes :D. Plan for tomorrow (today technically) is to get the baseline pcaps in so I can start writing the attacks finally... Plan is to probably do L2 attacks, then reverse it and try and defend against L2 attacks and so on until I finish with some application layer attacks and hopefully do an experiment with my own "C2 server."

29/05/2026
Made the Captures folder and inserted the baseline captures as well as the logs fromt the syslog server. Now that the baseline is complete, I can finally go about putting the Sec in NetSec :) I will most definitely make the attacks per layer and add other useful things into a newer and better .imn file and new baselines (think adding an HTTP server and a File server for higher level attacks). There should be a TODO/Ideas file added here so I can just keep my ideas for attacks in a dedicated spot instead of scattered all over my computer. I have no clue currently how or in what language these attacks will be in, but hey that's the importance of learning. I can say that I have learned a ton just from the configurations done up to this point and that I am very happy for going through with this project :D

31/05/2026
Nothing happened on github the past two days... I was spending some time finishing up the CDSA path (finally done woohooo) and reading into how scapy works... Turns out, these network attacks seem a lot easier than first expected! Can't wait to start making these scanners and attacks so stay tuned :)
