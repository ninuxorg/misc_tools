#!/usr/bin/env python2
# vim:ts=2:expandtab

import networkx as nx
import urllib2
import sys
import json

class InvalidOlsrJsonException(Exception):
  pass

class oneWayLink():
  "a one-way OLSR link"
  def __init__(self, linkDict):
    if linkDict == None:
            return
    if not linkDict.has_key('destinationIP') or not linkDict.has_key('lastHopIP') or not linkDict.has_key('linkQuality') or not linkDict.has_key('neighborLinkQuality') or not linkDict.has_key('tcEdgeCost'):
      raise InvalidOlsrJsonException
    self.__dict__.update(linkDict)

  def __repr__(self):
    return repr(self.__dict__)

  def aliased_link(self, destination, lasthop):
    "return a copy of the link with changed IP addresses"
    a = oneWayLink(None)
    a.__dict__.update(self.__dict__)
    a.destinationIP = destination
    a.lastHopIP = lasthop
    return a

class OlsrTopology():
  "an OLSR topology"
  linklist = []
  addressset = set()
  aliasdict = {}

  def __init__(self, urlorfile):
    self.urlorfile = urlorfile
    self.update_topology()
    self.update_gateways()

  def get_from_jsoninfo(self, urlappend):
    if self.urlorfile.startswith("http:"):
      # download 
      fno = urllib2.urlopen(self.urlorfile + urlappend, timeout=180)
    else:
      fno = open(self.urlorfile)
    json_topology = ("".join(fno.readlines())).strip()
    fno.close()
    
    # workaround for a bug in some versions of the jsoninfo plug-in
    if json_topology[0] != "{":
      json_topology = "{" + json_topology
    
    return json_topology
 
  def update_topology(self):
    json_mids = self.get_from_jsoninfo("/mid")
    aliaslist = json.loads(json_mids)['mid']
    for aliasdef in aliaslist:
      self.aliasdict[aliasdef['ipAddress']] = [ alias['ipAddress'] for alias in aliasdef['aliases'] ]

    json_topology = self.get_from_jsoninfo("/topology")
    topolist = json.loads(json_topology)['topology']

    # check for asymmetric links
    tmplinklist = [oneWayLink(ld) for ld in topolist]
    self.linklist = []
    for link in tmplinklist:
      reverselinks = [lnk for lnk in tmplinklist if lnk.destinationIP == link.lastHopIP and lnk.lastHopIP == link.destinationIP]
      assert len(reverselinks) == 1
      self.linklist.append(link)

    self.addressset = set([lnk.destinationIP for lnk in self.linklist] + [lnk.lastHopIP for link in self.linklist])

  def update_gateways(self):
    json_topology = self.get_from_jsoninfo("/hna")
    hnalist = json.loads(json_topology)['hna']

    self.gatewaylist = [hna['gateway'] for hna in hnalist if hna['destination'] == "0.0.0.0"]

  def is_in_topology(self, address):
    "returns true if the given IP address is a node of the topology graph"
    return address in self.addressset

  def is_gateway(self, address):
    return address in self.gatewaylist

  def getAliases(self, addr):
    if self.aliasdict.has_key(addr):
      return self.aliasdict[addr]
    else:
      return []

  def getMainAddress(self, addr):
    if self.aliasdict.has_key(addr):
      return addr
    for mainaddr, aliases in self.aliasdict.iteritems():
      for alias in aliases:
        if alias == addr:
          return mainaddr
    # assume it is a main address with no aliases (i.e. the only OLSR IP address of the node)
    return addr

  def get_shortest_path(self, u_source, u_destination):
    source = self.getMainAddress(u_source)
    destination = self.getMainAddress(u_destination)

    G = nx.DiGraph()
    #G.add_weighted_edges_from([(link.lastHopIP, link.destinationIP, 1 / (link.linkQuality * link.neighborLinkQuality)) for link in self.linklist])
    G.add_weighted_edges_from([(link.lastHopIP, link.destinationIP, link.tcEdgeCost) for link in self.linklist])

    if self.is_in_topology(source) and self.is_in_topology(destination):
      return nx.dijkstra_path(G, source, destination)
    elif self.is_in_topology(source):
      # find the closest gateway
      closestgw = None
      cost = 0
      for gw in self.gatewaylist:
        splen = nx.shortest_path_length(G, source, gw)
        if splen > cost:
          cost = splen
          closestgw = gw
      if closestgw:
        print "Warning: using gateway %s" % (closestgw,)
        return nx.dijkstra_path(G, source, closestgw)
      else:
        return None
    else:
      return None


if __name__ == "__main__":
        if len(sys.argv) < 4:
                print "Usage: %s <url or file> <source> <destination>"
                sys.exit(1)
        urlorfile = sys.argv[1]
        src = sys.argv[2]
        dst = sys.argv[3]
        t = OlsrTopology(urlorfile)
        for hop in t.get_shortest_path(src, dst):
          print hop + "\t (" + ", ".join(t.getAliases(hop)) + ")"


