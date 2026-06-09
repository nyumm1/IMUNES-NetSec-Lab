# ARP Spoof attack

Finally an attack and not a scanner!

This small python program uses Scapy to send gratuitous ARP packets that change (spoof) the MAC addresses of our machine so that we essentially get a MITM attack where the attacker can see all the traffic flowing between the victim and the victims gateway.

This works by first finding out all of the neccessary information for the attack: victim IP, victim MAC, gateway IP, gateway MAC, our IP, our MAC
After this is completed the tool then sends packets to both the gateway and the victim spoofing the packets to make sure that both the gateway and the victim communicate over the attacking computer, making it a computer in the middle :)
With this, the attacker can then use WireShark to scan all of the packets that the victim works with, which can be seen in the Captures!

A good note to myself might be to make this more of a shell script where the program after starting this .py file automatically opens something like tcpdump and starts printing to the user what is happening on the network.

## Usage
```bash
sudo python3 arpspoof.py <victimIP> <ourInterface>
```

## Output and damage

In the captures I ran the program off of FIN-pc2 with the following:
python3 10.0.20.20 eth0
Which means my victim was FIN-pc1 and my own interface used for the attack was eth0

With this I was able to successfully spoof the mac address and see all the data transmitted between FIN-pc1 and the rest of the network.
In the captures there is a youtube video, two dig commands and some other stuff... Main point was to show how invisible 2 ARP packets every ~2seconds is. In the .png file you can see the arp -n command ran before the spoof, during the spoof, and after the spoof with which you can clearly see the gateway and FIN-pc1 having the same MAC address.

I think that the damage of this entirely relies on the degree of which you can use the recorded data. Here, because of QUIC and https, you can't see what youtube video I'm playing at all (it was crab rave don't worry) neither can you see what else I was searching, but I'm sure that this in skilled hands can still give a ton of information to the attacker.
