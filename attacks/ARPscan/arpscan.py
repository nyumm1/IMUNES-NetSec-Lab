import sys
import time
import random
import ipaddress
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp1
from scapy.arch import get_if_addr
from scapy.config import conf

def validSubnet(subnet):
    try:
        ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


if len(sys.argv) !=3:
    print("Error! Usage: sudo python3 arpScan.py <subnet> <interface>")
    sys.exit(1)

subnet = sys.argv[1]
interface = sys.argv[2]

if not validSubnet(subnet):
    print("Error! Incorrect subnet input")
    sys.exit(1)

conf.iface = interface
sourceIP = get_if_addr(interface)

if sourceIP == "0.0.0.0":
    print("Error! Interface does not have an IP adress")
    sys.exit(1)

# The scanner

network = ipaddress.ip_network(subnet, strict=False)
hosts = list(network.hosts())
random.shuffle(hosts)

results = []

for ip in hosts:
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(ip), psrc=sourceIP)
    reply = srp1(packet, timeout=1, verbose=False, iface=interface)

    if reply:
        results.append((reply[ARP].psrc, reply[ARP].hwsrc))
        print(f"{reply[ARP].psrc}\t{reply[ARP].hwsrc}")
    
    time.sleep(random.uniform(1.0,2.0))

    


