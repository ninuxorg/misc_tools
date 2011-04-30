import smtplib, os
from email.mime.text import MIMEText

fromaddr = "servizioclienti@ninux.org"
toaddrs  = "contatti-roma@ninux.org"
monitored = {"NinuxFarm": '10.168.177.178' }
email = {
        'subject': (
                "Il nodo %s e' andato giu' ",
                "Il nodo %s e' tornato su' "
            ),
        'body' : (
                "Cara manica de pippe,\n il nodo %s e' andato giu \n\nServizio Clienti Ninux.org",
                "Cara manica de pippe,\n Il nodo %s e' tornato su \n\nServizio Clienti Ninux.org"
            )
        }
pingcmd = "ping -c 1 "

def get_state():
    in_file = open("farm_state.txt","r")
    farm_state = in_file.read()
    in_file.close()
    return farm_state

def set_state(state):
    out_file = open("farm_state.txt","w")
    out_file.write(state)
    out_file.close()

def send_notification(name, status):
    '''
        name = nome del nodo
        status = 0,1  ---> OFF, ON
    '''
    global fromaddr, toaddrs, email
    print "Sending email..."
    msg = MIMEText(email['body'][status] % name)
    msg['Subject'] = email['subject'][status] % name 
    msg['From'] = fromaddr
    msg['To'] = toaddrs 

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg.as_string() )
    server.quit()

for name,ip in monitored.items():
    ping_status = os.system(pingcmd + ip) # 0-> up , >1 down
    previous_state = get_state()
    print "----"
    print ( ping_status, previous_state )
    print "----"
    if ping_status > 0 and previous_state.find("on") >= 0: 
        send_notification(name, 0)
        set_state('off')

    elif ping_status == 0 and previous_state.find("off") >= 0:
        send_notification(name, 1)
        set_state('on')

