import smtplib, os, time 
from email.mime.text import MIMEText
import MySQLdb
import re, textwrap
    
fromaddr = "contatti@ninux.org"
email_first = '''Caro %s referente per il nodo %s della rete
ninux.org, ricevi questa mail in quanto %s
'''

email_last = '''

---- SHORT VERSION ----

Ninux ti invita Sabato 21 Maggio ore 11:00 presso i locali del CSOA
Sans Papier, via Carlo Felice 69 per la Ninux Academy. Presentazioni e
seminari sul progetto Ninux.org, come costruire il proprio nodo, come
mantenerlo e vivere felici dentro la nostra rete :)

Per vedere il programma completo:
http://wiki.ninux.org/NinuxAcademy2011

---- LONG VERSION ----

Dopo una fase pionieristica di sperimentazione e progettazione la
comunita' ninux.org e' decisamente passata alla fase di realizzazione
della rete; i nodi attivi sono aumentati e cosi' le zone raggiunte,
anche fuori Roma. Ogni giorno si accendono nuovi nodi e vecchi nodi
potenziali sono ora nodi attivi funzionanti e partecipi a questo progetto
di liberta'. Puoi vedere tu stesso l'avanzamento della rete attraverso
il map server all'indirizzo http://map.ninux.org/

Ora vogliamo fare un ulteriore salto e cercare di trasformare l'interesse
dei tanti che, come te, lo hanno manifestato da piu' o meno tempo,
in una collaborazione informata, consapevole e partecipata.

Stiamo preparando per il 21 Maggio un incontro per condividere quello
che abbiamo imparato e porre le basi per un allargamento della rete.
In questo incontro racconteremo cosa e' la rete ninux, come vorremmo
svilupparla, qual e' lo spirito della community; vedremo insieme
nella pratica le tecniche per allestirsi da soli il proprio nodo,
come identificare un possibile vicino con cui collegarsi, quali sono le
situazioni favorevoli e quelle da evitare per far rendere al meglio il
collegamento; materiali, apparati, configurazioni, cablaggi, ferramenta
e strumenti di ausilio alla installazione.

Per chi e' gia' all'interno della rete, vedremo con quali semplici comandi
sia possibile diagnosticare lo stato del proprio nodo e risolvere da
soli i problemi piu' comuni che possono insorgere nel suo funzionamento
quotidiano.

Per il programma completo ti rimandiamo al nostro wiki:

http://wiki.ninux.org/NinuxAcademy2011

Ti invitiamo a raggiungerci Sabato 21 Maggio a partire dalle 11:00,
presso i locali del CSOA Sans Papier, via Carlo Felice 69


La community ninux.org

--
http://www.ninux.org (sito)
http://blog.ninux.org/ (blog)
'''

conn = MySQLdb.connect(host="10.0.1.1", user="wnmap", passwd="XXXXX", db="wnmapunstable")
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
        reason = "hai segnalato alla community il tuo interesse a farne parte, registrandoti sulla mappa e lasciando questo recapito."
    if email_list.has_key(record[2]):
        email_list[record[2]]['node_name'].append( ", " + str(record[0]) + " (" + node_status + ")" ) 
        if node_status != 'potenziale' :
            email_list[record[2]]['reason'] = reason 
    else:
        email_list[record[2]] = {'name': record[3], 'reason': reason, 'node_name': [ str(record[0]) + " (" + node_status + ")"] }
   
for k, v in email_list.items():
    print "Sending email to " + k
    msg = MIMEText(textwrap.fill( email_first % ( v['name'], ' '.join(v['node_name']) , v['reason'] ), 72) + email_last )
    msg['Subject'] = 'Ninux.org ti invita alla Ninux Academy'
    msg['From'] = fromaddr
    #k = 'lorenzo.bracciale@uniroma2.it'
    msg['To'] = k 

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, k , msg.as_string() )
    server.quit()
    print "sent to " + k + "\n" 
    time.sleep(1)

