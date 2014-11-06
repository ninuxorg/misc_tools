#!/usr/bin/env python
# An example script that shows how to parse an OLSR topology and feed it to networkx

import networkx as nx
import urllib2 
import json

# OLSR JSON plug-in URL
#OLSR_TOPOLOGY = "http://127.0.0.1:9090"
OLSR_TOPOLOGY = "http://10.132.1.1:9090"

# download the topology
fno = urllib2.urlopen(OLSR_TOPOLOGY + "/topology", timeout=180)
# join all lines from the json plug-in output
json_topology = ("".join(fno.readlines())).strip()
# transform json into a list of dicts
topolist = json.loads(json_topology)['topology']

G = nx.DiGraph() 
# add edges in the form (node1, node2, ETX)
G.add_weighted_edges_from([(link['lastHopIP'], link['destinationIP'], link['tcEdgeCost']) for link in topolist])

# apply algorithms and functions
# https://networkx.github.io/documentation/networkx-1.9.1/reference/algorithms.html
# https://networkx.github.io/documentation/networkx-1.9.1/reference/functions.html
print nx.info(G)

