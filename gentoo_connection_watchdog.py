# Add this using "crontab -e"
# */5 * * * * python /root/gentoo_connection_watchdog.py > /dev/null 2>&1


import os
import sys
import time
import smtplib

#implement watchdog for IPv6 that just restarts aiccu

if (os.system("ping -c 1 www.google.com") !=0):
	os.system("/etc/init.d/net.ppp0 restart")
	time.sleep(10)
	#restore IPv6
	os.system("killall -9 aiccu")
	print "start aiccu\n"
	os.system("/usr/sbin/aiccu start")
	server = smtplib.SMTP('localhost')
	server.set_debuglevel(0)
	server.sendmail("tuscoloserver@ninux.org", "zioproto@ninux.org", "Server al Tuscolo senza connessione, restaring")
	server.quit()

