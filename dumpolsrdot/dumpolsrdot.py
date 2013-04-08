#!/usr/bin/env python

#dumps the current OLSR topology in dot format (using the dot_draw plugin) to standard output

import telnetlib
import sys

def readfromdotplugin(host='127.0.0.1',port='2004',timeout=120, exitonerror=True):
        try:
                dotcon=telnetlib.Telnet(host,port)
        except:
                sys.stderr.write("Error. Can't connect to %s:%s.\n" % (host,port))
                if exitonerror:
                        sys.exit(2)
                else:
                        return ""
        dotoutput=""
        dotoutput=dotcon.read_until('}',timeout)
        dotoutput+='\n'
        dotcon.close()
        return dotoutput
#readfromdotplugin

if __name__=="__main__":
        print readfromdotplugin()
