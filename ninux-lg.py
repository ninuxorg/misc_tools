#! /usr/bin/env python
import os
import sys
import IPy
from IPy import IP

try:
	ipaddress = IP(sys.argv[1])
	if (ipaddress.version() ==4):
		port = 2006
		version = 4

	if (ipaddress.version() ==6):
		port = 2007
		version = 6
except:
	print "invalid IP address"
	sys.exit(-1)
"""
	Possible tables:
	Table: Links
	Table: Neighbors
	Table: Topology
	Table: HNA
	Table: MID
	Table: Routes
"""
try:
	cmd = sys.argv[2]
except:
	cmd = "all"

if (version == 4):
	os.system("wget -q http://"+ipaddress.strNormal()+":"+str(port)+"/"+cmd+" -O -")

if (version == 6):
	os.system("wget http://["+ipaddress.strNormal()+"]:"+str(port)+"/"+cmd+" -O -")


