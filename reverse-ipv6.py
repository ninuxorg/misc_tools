#! /usr/bin/env python
import os
import sys
import IPy
from IPy import IP
# aptitude install python-ipy

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

print ipaddress.reverseName()

