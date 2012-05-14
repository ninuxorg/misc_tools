import os 
import sys
import time
import smtplib
import datetime

from settings import *

def logToFile(string,logfile):
	f=open(logfile,'a')
	f.write(str(datetime.datetime.now())+string+"\n")
	f.close()


while True:
	if (os.system("ping6 -c 1 -r "+IPtocheck+" > /dev/null") !=0):
		if (os.system("ping6 -c 1 -r "+IPtocheck+" > /dev/null") !=0):
			if (os.system("ping6 -c 1 -r "+IPtocheck+" > /dev/null") !=0):
			        server = smtplib.SMTP(smtpserver)
	        		server.set_debuglevel(0)
				msg = "From:"+fromemail+"\r\nTo:"+toemail+"\r\nSubject:"+subject
	        		logToFile(body,logfile)
				server.sendmail(fromemail, toemail, msg)
	        		server.quit()
				time.sleep(30)
	else:
		time.sleep(2)

