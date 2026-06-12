# Port scan 

Small TCP syn port scanner made with Scapy.

It comes with the following options:
- By default, it scans the Top 100 ports
- with --all it scans all of the ports
- with --range it scans from a to b ports
- with --ports it scans the specific ports

Made with some new tech (to me), it features threading and ThreadPoolExecutor to speed up the scanning process and uses argparse for the input and option parsing. Speed wise, it's quite slower than nmap but I'm quite sure it's down to nmap being written in C :)

## Usage
```bash
sudo python3 portScan.py <target IP address> <options>
```

## Output

With the scan of:
- python3 portScan.py 10.0.30.20
from HR-pc2 it produced these outputs:
- 21 OPEN
- 22 OPEN
- 23 OPEN

and with the scan of:
- python3 portScan.py 10.0.10.11
from HR-pc2 it produced these outputs:
- 53 OPEN
- 111 OPEN

Very happy with how this small scanner turned out, next idea could be adding UDP support or different TCP scan support :)


