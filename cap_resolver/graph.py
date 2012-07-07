#!/usr/bin/env python

# Copyright (c) 2012 Claudio Mugnanti
# CAP 2 NinuxAddress RESOLVER - graph utils
# require: http://code.google.com/p/python-graph/wiki/Example


# Import graphviz
import sys
import csv
import gv

# Import pygraph
# sudo easy_install python-graph-dot
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

gr = graph()

# Add nodes for cap
#gr.add_nodes(range(255))

#gr.add_edge(("Portugal", "Spain"))
#read the cap file as per http://lab.comuni-italiani.it/download/comuni.html

#only e subset of city are render. The full map si too large
citylist = ["Pisa", "Roma", "Ostia", "Zagarolo", "Ladispoli", "Catanzaro", "Trieste", "Pomezia",
	"Viterbo", "Manziana", "Montecatini terme", "Carrara", "Cosenza", "Reggio Calabria", "Mistretta",
	"Vittoria", "Lecce", "Foggia", "Pescara", "Reggello", "Verona", "Monza", "Stregna" #questo vince su tutti
	, "", "", "", "", "", "", "", "", "", ""]

capfile = csv.reader(open('listacomuni.txt', 'rb'), delimiter=';', quotechar='"')
for tupla in capfile:
## formato
##Codice Istat; Nome Comune; Sigla Provincia; Sigla Regione; 
##Prefisso Telefonico; CAP; Codice Catastale (codice fisco); Abitanti; Link Pagina Info
	city = unicode(tupla[1], errors='ignore')
	if city not in citylist:
		continue

	print city
	print tupla[5]
	try:
		gr.add_nodes([city])
	except:
		pass


	tupla[5] = tupla[5].replace('x', '0')
	cap = int(tupla[5])
	#real resolver  FIXME to be implemented
	if(int(tupla[5])  > 1000):
		ncap = cap %255
	else:
		ncap = cap % 255

	try:
		gr.add_nodes([ncap])
	except:
		pass

	try:
		gr.add_edge( (ncap, city) )
	except:
		pass
	

# Draw as PNG
dot = write(gr)
gvv = gv.readstring(dot)
gv.layout(gvv,'dot')
gv.render(gvv,'png','cap_ninux.png')
