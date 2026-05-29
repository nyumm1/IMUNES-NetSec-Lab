# IMUNES-NetSec-Lab

> A small playground for testing, learning, and experimenting with networking
> and security concepts while getting more comfortable with IMUNES.

---

## The Playground

The goal of this lab was to create a small office-style network where different
networking and security concepts can be tested, explored, and configured in a
way that resembles a real office environment.

The network is divided into 5 distinct subsections:

### Server Subnet

Contains the core services typically required in a small office environment:

- DHCP Server
- DNS Server
- File Server
- Web Server

### Department Subnets

Three similar subnets representing different departments within the organization:

- Finance
- IT
- HR

### Management Subnet

A separate management network containing:

- 1 Management PC
  - Used as the attacker machine for most security tests

- SYSLOG Server
  - Collects and stores logs from across the network

---

## Network Topology

Each subnet connects to its own subnet router, and all subnet routers connect
to a central main/master router.

The master router is responsible for communicating with the outside network
through the `rj45-1` connection.

---

## Purpose of the Lab

This environment is intended to be used for:

- Networking practice
- Security experimentation
- Service configuration
- Routing and subnetting practice
- Logging and monitoring tests
- General IMUNES learning and exploration

---

## Notes

This project is still a work in progress, and some configurations are currently
implemented with varying levels of success... Pls be patient with me :)
