#! /usr/bin/env python
import os
from subprocess import Popen, PIPE, STDOUT

cmd = "gpg --list-keys | grep pub |grep -v gnupg | cut -c 13-20"
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

tmp = p.stdout.readline()
while tmp:
	os.system("gpg --keyserver pgp.mit.edu --send-key " + tmp)
	os.system("gpg --keyserver pool.sks-keyservers.net --send-key " + tmp)
	os.system("gpg --keyserver keyserver.linux.it --send-key " + tmp)
	tmp = p.stdout.readline()



