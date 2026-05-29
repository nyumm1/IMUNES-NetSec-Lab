# Baseline network capture 

This is a simple baseline capture which will be later used (hopefully) to better see and understand the difference between normal and malicious traffic.

---

## 1. Traffic Generation (FIN-pc1)

All traffic was generated from `FIN-pc1` using the following commands:

- `ping 10.0.10.11` (DNS server)
- `ping 10.0.30.20` (HR-pc1 inter-department)
- `dig web-server.office.lan` (DNS query)
- `dig fin-pc1.office.lan` (reverse lookup)
- `ping 10.0.50.10` (syslog server)
- `dig google.com` (external DNS resolution)

---

## 2. Capture Points

Packet captures were collected at the following interfaces:

### MAIN-router eth1 (Main -> Server router)
- DNS traffic (internal queries and responses)
- Server-bound communication

### MAIN-router eth2 (Main -> Finance router)
- Traffic originating from FIN subnet

### MAIN-router eth5 (Main -> Management router)
- Syslog server routes most importantly

### HR-router eth0 (HR subnet)
- Mostly quiet local subnet, best for baseline

---

## 3. Syslog Data

Syslog exports are stored in `/logs`
