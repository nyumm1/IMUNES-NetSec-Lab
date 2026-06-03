# ARP scan 

A small "stealthy" ARP host scan built with Scapy.

The scanner sends ARP requests to each host in the specified subnet and collects replies to map out active hosts and their MAC addresses.
I tried making it more "stealthy" by shuffling the requested packets as well as with putting a random sleep time of 1-2 seconds between each scan... This way it looks a tad more like normal traffic.

## Usage
```bash
sudo python3 arpscan.py <subnet> <interface>
```

## Output

With the scan of:
- sudo python3 arpscan.py 10.0.40.0/27 eth0

It had found all 4 of the active hosts within the IT subnet when started on IT-pc1:
- IT-router
- IT-pc2
- IT-pc3
- IT-pc4

Only problem I saw is that when it came to ask for the address 10.0.40.20 (the address of IT-pc1) then it gave an ARP announcement which I think is an easy way to spot this simple scanner? Will definitely try to block this with a firewall in the future!

