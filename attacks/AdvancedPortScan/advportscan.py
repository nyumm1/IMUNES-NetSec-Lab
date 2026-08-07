from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.sendrecv import sr1
import argparse
import ipaddress
import sys
from concurrent.futures import ThreadPoolExecutor
import socket

TOP_100_PORTS = [1, 7, 9, 13, 17, 19, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514, 515, 543, 544, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026, 1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049, 2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060, 5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070, 8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152, 49153, 49154, 49155, 49156, 49157, 51820]

def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
def get_service(port, protocol): # added because program would crash if service wasn't known
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return "unknown"

   
def scan_port(target, port, scan_type, timeout=None):
    if scan_type == "syn":
        packet = IP(dst=target) / TCP(dport=port, flags="S")
        reply = sr1(packet, timeout=timeout or 0.5, verbose=False)
        if reply and reply.haslayer(TCP):
            flags = reply[TCP].flags
            if flags == "SA":
                return(port, f"{port}/tcp", "OPEN", get_service(port, "tcp"))
            elif flags == "R":
                return(port, f"{port}/tcp", "CLOSED", get_service(port, "tcp"))
            
    elif scan_type in ("null", "fin", "xmas"):
        flags = { "null" :  "", "fin": "F", "xmas": "FPU"}[scan_type]
        packet = IP(dst=target) / TCP(dport=port, flags = flags)
        reply = sr1(packet, timeout=timeout or 0.5, verbose=False)
        if reply is None:
            return(port, f"{port}/tcp", "OPEN|FILTERED", get_service(port, "tcp"))
        elif reply.haslayer(TCP) and reply[TCP].flags in ("R", "RA"):
            return(port, f"{port}/tcp", "CLOSED", get_service(port, "tcp"))
        
    elif scan_type == "udp":
        packet = IP(dst = target) / UDP(dport=port)
        reply = sr1(packet, timeout=timeout or 2, verbose=False)
        if reply is None:
            return(port, f"{port}/udp", "OPEN|FILTERED", get_service(port, "udp"))
        elif reply.haslayer(ICMP):
            if int(reply[ICMP].type) == 3 and int(reply[ICMP].code) == 3:
                return(port, f"{port}/udp", "CLOSED", get_service(port, "udp"))
        elif reply.haslayer(UDP):
            return(port, f"{port}/udp", "OPEN", get_service(port, "udp"))

    return None

def _build_arg_parser():
    parser = argparse.ArgumentParser(description="Advanced, but still Small, Port Scanner")
    parser.add_argument("target", help="Target IP address")

    # port input types (alongside the default)
    parser.add_argument("--all", action="store_true", help="Scan all ports")
    parser.add_argument("--range", help="Port range, e.g. 1-1024")
    parser.add_argument("--ports", help="Specific ports, e.g. 22,53,80,443")

    # added, new scan types
    parser.add_argument("--syn", action="store_true", help="TCP SYN scan (default scan)")
    parser.add_argument("--null", action="store_true", help="TCP NULL scan")
    parser.add_argument("--fin", action="store_true", help="TCP FIN scan")
    parser.add_argument("--xmas", action="store_true", help="TCP XMAS scan")
    parser.add_argument("--udp", action="store_true", help="UDP scan")
    return parser


def format_results(results):
    lines = []
    for _port, portproto, status, service in results:
        lines.append(f"{portproto:<12}{status:<15}{service}")
    return "/n".join(lines)

def scan(target, ports=None, scan_type="syn", max_workers=None, timeout=None):
    if not valid_ip(target):
        raise ValueError(f"Invalid IP address: {target}")

    if scan_type not in ("syn", "null", "fin", "xmas", "udp"):
        raise ValueError(f"Invalid scan_type: {scan_type}")

    if ports is None:
        ports = TOP_100_PORTS

    if max_workers is None:
        max_workers = 10 if scan_type == "udp" else 100

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, target, p, scan_type, timeout) for p in ports]
        results = [f.result() for f in futures]

    results = [r for r in results if r is not None]
    return sorted(results, key=lambda r: r[0])

def _parse_ports_arg(args):
    if args.all:
        return list(range(0,65536))
    elif args.range:
        lo, hi = args.range.split("-")
        return list(int(lo), int(hi))
    elif args.ports:
        return [int(p) for p in args.ports.split(",")]
    return TOP_100_PORTS

def _parse_scan_type_arg(args):
    if args.null:
        return "null"
    elif args.fin:
        return "fin"
    elif args.xmas:
        return "xmas"
    elif args.udp:
        return "udp"
    return "syn"

def main(argv=None):
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if not valid_ip(args.target):
        print("Error! Invalid IP address")
        sys.exit(1)

    ports = _parse_ports_arg(args)
    scan_type = _parse_scan_type_arg(args)

    results = scan(args.target, ports=ports, scan_type=scan_type)
    print(format_results(results))


if __name__ == "__main__":
    main()





