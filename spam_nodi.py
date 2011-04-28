import smtplib, os
from email.mime.text import MIMEText
import MySQLdb
import re
    
fromaddr = "contatti@ninux.org"
email_text = '''
Caro %s referente per il nodo %s della rete
ninux.org, ricevi questa mail in quanto %s

Come avrai forse potuto vedere, dopo una fase pionieristica di
sperimentazione e progettazione la comunita' ninux.org e' decisamente
passata alla fase di realizzazione della nostra rete wireless; i nodi
attivi sono aumentati e cosi' le zone raggiunte, anche fuori Roma. Ogni
giorno si accendono nuovi nodi e vecchi nodi potenziali sono ora nodi
attivi funzionanti e partecipi a questo grande progetto di liberta'.
Puoi vedere tu stesso l'avanzamento della rete attraverso il map server 
all'indirizzo http://map.ninux.org/ .

Ora vogliamo fare un ulteriore salto e cercare di trasformare
l'interesse dei tanti che, come te, lo hanno manifestato da piu' o meno
tempo, in una collaborazione informata, consapevole e fattiva.

Stiamo preparando per il 21 Maggio un incontro per condividere, con tutte le persone interessate al nostro progetto, quello che abbiamo imparato e porre le basi per un
allargamento del gruppo.
In questo incontro spiegheremo cosa e' la rete ninux, come vorremmo
svilupparla, qual e' lo spirito della community; illustreremo le tecniche
per allestirsi da soli il proprio nodo, come identificare un possibile
vicino con cui collegarsi, quali sono le situazioni favorevoli e quelle
da evitare per far rendere al meglio il collegamento; materiali,
apparati, configurazioni, cablaggi, ferramenta e strumenti di ausilio
alla installazione.

Spiegheremo con quali semplici comandi sia possibile diagnosticare lo 
stato del proprio nodo e risolvere da soli i problemi piu' comuni che 
possono insorgere nel suo funzionamento quotidiano.

Per coloro piu' interessati invece ai protocolli di rete illustreremo
tutti quelli che hanno un ruolo nella nostra rete; e siccome ninux e' gia'
predisposta per la IPv6, includeremo un accenno anche al nuovo
protocollo della rete Internet.

Ovviamente saremo a disposizione per qualsiasi dubbio o domanda di
approfondimento tu voglia farci e che possa contribuire a farti
comprendere meglio, sotto ogni punto di vista, cosa e' ninux, cosa puo'
dare e quali ne sono i confini che vi abbiamo stabilito.

Pertanto, se ritieni che la tua adesione come potenziale nodo possa
evolvere, ti invitiamo a raggiungerci Sabato 21 Maggio a partire dalle
14.00, presso i locali del CSOA Sans Papier, via Carlo Felice 69 

Un cordiale arrivederci.

La community ninux.org


http://www.ninux.org (sito)
http://blog.ninux.org/ (blog)
'''

conn = MySQLdb.connect(host="10.0.1.1", user="wnmap", passwd="XXXX", db="wnmapunstable")
cursore = conn.cursor()
link_cursore = conn.cursor()
cursore.execute('SELECT nodeName, status, userEmail, userRealName FROM nodes')
email_list = {}
node_status, reason = "", ""
for record in cursore.fetchall():
    if record[1] == 2:
        node_status = 'attivo'
        reason = "partecipante attivo della community."
    elif record[1] == 3:
        node_status = 'hotspot'
        reason = "partecipante attivo della community."
    else:
        node_status = 'potenziale'
        reason = "hai segnalato alla nostra community il tuo interesse a farne parte, registrandoti sulla mappa e lasciando questo recapito."
    if email_list.has_key(record[2]):
        email_list[record[2]]['node_name'].append( ", " + str(record[0]) + " (" + node_status + ")" ) 
        if node_status != 'potenziale' :
            email_list[record[2]]['reason'] = reason 
    else:
        email_list[record[2]] = {'name': record[3], 'reason': reason, 'node_name': [ str(record[0]) + " (" + node_status + ")"] }
   
for k, v in email_list.items():
    print "Sending email to " + k
    msg = MIMEText(email_text % ( v['name'], ' '.join(v['node_name']) , v['reason'] ) )
    msg['Subject'] = 'Ninux.org ti invita alla Ninux Academy'
    msg['From'] = fromaddr
    k = 'contatti-roma@ninux.org'
    msg['To'] = k 

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, k , msg.as_string() )
    server.quit()
    print msg
    break

