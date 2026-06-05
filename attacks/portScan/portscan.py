from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1
import argparse
import ipaddress
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Small Port Scanner")
parser.add_argument("target", help="Target IP address")
parser.add_argument("--all", action="store_true", help="Scan all ports")
parser.add_argument("--range", help="Port range, e.g. 1-1024")
parser.add_argument("--ports", help="Specific ports, e.g. 22,53,80,443")


TOP_100_PORTS = [1, 7, 9, 13, 17, 19, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157]

def validIP(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
lock = threading.Lock()    
def scanPort(port):
    packet = IP(dst=args.target) / TCP(dport=port, flags="S")
    reply = sr1(packet, timeout=0.5, verbose=False)
    if reply and reply.haslayer(TCP):
        flags = reply[TCP].flags

        if flags == "SA":
            with lock:
                print(str(port) + " OPEN")
        elif flags == "R":
            with lock:
                print(str(port) + " CLOSED")    
    
args = parser.parse_args()
ports = []

if not validIP(args.target):
    print("Error! Invalid IP address")
    sys.exit(1)


if args.all:
    ports = range(0,65536)
elif args.range:
    tmp = args.range.split("-")
    ports = range(int(tmp[0]), int(tmp[1]))
elif args.ports:
    tmp = args.ports.split(",")
    for port in tmp:
        ports.append(int(port))
else:
    ports = TOP_100_PORTS

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scanPort, ports)




