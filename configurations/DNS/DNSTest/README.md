# DNS Test

Another proof of concept test to better understand the ways that DNS is configured on the network. Written completely by myself now (take that claude!) and working with Bind9, it functions as intended with one forwarding zone (db.lab.lan) and 6 reversing zones (db.reverse.x) which are all just filled with PTRs to the addresses

Hardest part about this DNS config was not making a typo while typing all of the necessarry files :P
For real now, the hardest part was understanding the way that this network gets configured... And I mean that in the way of understanding where to put what part of the DNS "machine" so that it all works out in the end.

Now the next step will be pouring over all the things learned from the DNSTest into my main office topology and setting it all up... I still think that making a config script for this makes tons of sense as typing sudo hcp blah blah like 10 times makes zero sense...

Anyways, this is now finished and the project can be taken and put into imunes and it will work with starting named -c /etc/bind/named.conf in the pc terminal after putting all of the files where they have to go... Best check where they need to go by reading the named.conf.local!
