#!/usr/bin/env python

#Copy this file somewhere in /usr/bin, make it executable, and specify this file in squid.conf as url_rewrite_program
#This will make any request for the google home page go to your splash page at 10.10.0.1 (it is assumed you have a squid transparent proxy setup)

import sys
def modify_url(line):
    list = line.split(' ')
    # first element of the list is the URL
    old_url = list[0]
    new_url = '\n'
    # take the decision and modify the url if needed
    # do remember that the new_url should contain a '\n' at the end.
    if (old_url.find("www.google") != -1 and old_url.find("=") == -1 and old_url.find("calendar") == -1 and old_url.find("?") == -1 and old_url.find("trends")):
        new_url = '301:http://10.10.0.1/' + new_url
    return new_url
 
while True:
    # the format of the line read from stdin is
    # URL ip-address/fqdn ident method
    # for example
    # http://saini.co.in 172.17.8.175/saini.co.in - GET -
    line = sys.stdin.readline().strip()
    # new_url is a simple URL only
    # for example
    # http://fedora.co.in
    new_url = modify_url(line)
    sys.stdout.write(new_url)
    sys.stdout.flush()
