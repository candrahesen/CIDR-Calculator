#!/usr/bin/env python

import socket

def ipToInt(host):
	iphost1 = host.split('.')[0]
	iphost2 = host.split('.')[1]
	iphost3 = host.split('.')[2]
	iphost4 = host.split('.')[3]
	host1 = int(iphost1)
	host2 = int(iphost2)
	host3 = int(iphost3)
	host4 = int(iphost4)
	result = (16777216 * host1) + (65536 * host2) + (256 * host3) + host4
	return result

def recv_until(conn, str):
	buf = ''
	while not str in buf:
		buf += conn.recv(1)
	return buf

def getValidSubnet(host):
	return '0.0.0.0/0'

def countHosts(subnet):
	subnetmask = subnet.split("/")[-1]
	angka = int(subnetmask)
	return str(2**(32-angka))

def isSubnetValid(subnet, host):
	hhost = ipToInt(host)

	ipsubnet = subnet.split("/")[0]
	subnetmask = subnet.split("/")[-1]

	intipsubnet = ipToInt(ipsubnet)
	intsubnetmask = int(subnetmask)

	mask = (0xffffffff << (32-intsubnetmask)) & 0xffffffff

	if ((hhost & mask) == (intipsubnet & mask)):
		return 'T'
	else:
		return 'F'
	
TCP_IP = 'hmif.cf'
TCP_PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

data = recv_until(s, 'NIM: ')
nim = raw_input(data)
s.send(nim + '\n')

data = recv_until(s, 'Verify NIM: ')
nim = raw_input(data)
s.send(nim + '\n')

print recv_until(s, '\n')[:-1]

# Phase 1
for i in range(100):
	recv_until(s, 'Host: ')
	host = recv_until(s, '\n')[:-1]
	recv_until(s, 'Subnet: ')
	s.send(getValidSubnet(host) + '\n')
print recv_until(s, '\n')[:-1]

# Phase 2
for i in range(100):
	recv_until(s, 'Subnet: ')
	subnet = recv_until(s, '\n')[:-1]
	recv_until(s, 'Number of Hosts: ')
	s.send(countHosts(subnet) + '\n')
print recv_until(s, '\n')[:-1]

# Phase 3
for i in range(100):
	recv_until(s, 'Subnet: ')
	subnet = recv_until(s, '\n')[:-1]
	recv_until(s, 'Host: ')
	host = recv_until(s, '\n')[:-1]
	s.send(isSubnetValid(subnet, host) + '\n')
print recv_until(s, '\n')[:-1]

s.close()
