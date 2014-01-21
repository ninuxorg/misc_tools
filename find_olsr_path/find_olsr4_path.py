#!/usr/bin/env python2
# vim:ts=2:expandtab
#
#  Copyright 2013 Claudio Pisa (clauz at ninux dot org)
#
#  This file is part of find_olsr_path
#
#  find_olsr_path is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  find_olsr_path is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with find_olsr_path.  If not, see <http://www.gnu.org/licenses/>.
#


import networkx as nx
import urllib2
import sys
import json

verbose = False

def printout(string):
    if verbose:
        print string


class InvalidOlsrJsonException(Exception):
  pass


class oneWayLink():
  "a one-way OLSR link"
  def __init__(self, linkDict=None):
    if linkDict == None:
            return
    if not linkDict.has_key('destinationIP') or not linkDict.has_key('lastHopIP') or not linkDict.has_key('linkQuality') or not linkDict.has_key('neighborLinkQuality') or not linkDict.has_key('tcEdgeCost'):
      raise InvalidOlsrJsonException
    self.__dict__.update(linkDict)

  def __repr__(self):
    return repr(self.__dict__)

  def aliased_link(self, destination, lasthop):
    "return a copy of the link with changed IP addresses"
    a = oneWayLink()
    a.__dict__.update(self.__dict__)
    a.destinationIP = destination
    a.lastHopIP = lasthop
    return a

class Hna():
  "an OLSR HNA entry"
  def __init__(self, linkDict):
    if linkDict == None:
            return
    if not linkDict.has_key('destination') or not linkDict.has_key('genmask') or not linkDict.has_key('gateway'):
      raise InvalidOlsrJsonException
    self.__dict__.update(linkDict)

  def __repr__(self):
    return repr(self.__dict__)

  def __dotted_decimal_2_int(self, ip_address):
    dotteddecimals = ip_address.split('.')
    bip = 0
    for d in dotteddecimals:
        i = int(d)
        bip = bip << 8
        bip += i
    return bip

  def ip_in_net(self, ip_address):
    "return True iff ip_address belongs to this HNA"
    bip = self.__dotted_decimal_2_int(ip_address)
    bnet = self.__dotted_decimal_2_int(self.destination)
    l = self.genmask
    bmask = int("0b" + "1" * l + "0" * (32-l), 2)
    return bip & bmask == bnet


class OlsrTopology():
  "an OLSR topology"
  linklist = []
  addressset = set()
  aliasdict = {}
  hnalist = []

  def __init__(self, urlorfile):
    self.urlorfile = urlorfile
    self.update_topology()
    self.update_mids()
    self.update_hnas()
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
    json_topology = self.get_from_jsoninfo("/all")
    topolist = json.loads(json_topology)['topology']

    # check for asymmetric links
    tmplinklist = [oneWayLink(ld) for ld in topolist]
    self.linklist = []
    for link in tmplinklist:
      reverselinks = [lnk for lnk in tmplinklist if lnk.destinationIP == link.lastHopIP and lnk.lastHopIP == link.destinationIP]
      assert len(reverselinks) == 1
      self.linklist.append(link)

    # add ourselves to the graph
    mainaddr = json.loads(json_topology)['config']['mainIpAddress']
    directlinklist = json.loads(json_topology)['links']
    for dl in directlinklist:
        # direct link
        owl1 = oneWayLink()
        owl1.lastHopIP = mainaddr
        owl1.destinationIP = dl['remoteIP']
        owl1.linkQuality = dl['linkQuality']
        owl1.neighborLinkQuality = dl['neighborLinkQuality']
        owl1.tcEdgeCost = dl['linkCost']

        # reverse link
        owl2 = oneWayLink()
        owl2.lastHopIP = owl1.destinationIP
        owl2.destinationIP = owl1.lastHopIP
        owl2.linkQuality = owl1.neighborLinkQuality
        owl2.neighborLinkQuality = owl1.linkQuality
        owl2.tcEdgeCost = owl1.tcEdgeCost

        self.linklist.append(owl1)
        self.linklist.append(owl2)

    self.addressset = set([lnk.destinationIP for lnk in self.linklist] + [lnk.lastHopIP for link in self.linklist])

  def update_mids(self):
    json_mids = self.get_from_jsoninfo("/all")
    aliaslist = json.loads(json_mids)['mid']
    for aliasdef in aliaslist:
      self.aliasdict[aliasdef['ipAddress']] = [ alias['ipAddress'] for alias in aliasdef['aliases'] ]

    interfacelist = json.loads(json_mids)['interfaces']
    if len(interfacelist) < 2:
        return
    mainaddr = json.loads(json_mids)['config']['mainIpAddress']
    self.aliasdict[mainaddr] = []
    for interface in interfacelist:
        ipaddr = interface['ipv4Address']
        if mainaddr != ipaddr:
            self.aliasdict[mainaddr].append(ipaddr)

  def update_hnas(self):
    json_hnas = self.get_from_jsoninfo("/all")
    hnalist = json.loads(json_hnas)['hna']
    for hna in hnalist:
      self.hnalist.append(Hna(hna))

    localhnalist = json.loads(json_hnas)['config']['hna']
    for hna in localhnalist:
      self.hnalist.append(Hna(hna))

  def update_gateways(self):
    json_hnas = self.get_from_jsoninfo("/all")
    hnalist = json.loads(json_hnas)['hna']
    localhnalist = json.loads(json_hnas)['config']['hna']

    self.gatewaylist = [hna['gateway'] for hna in hnalist + localhnalist if hna['destination'] == "0.0.0.0"]

  def is_gateway(self, address):
    return address in self.gatewaylist

  def getAliases(self, addr):
    if self.aliasdict.has_key(addr):
      return self.aliasdict[addr]
    else:
      return []

  def getHnaGateway(self, addr):
    """if the IP address belongs to an HNA then return the IP address 
    of the node announcing the HNA. Else return addr."""
    gwresult = addr
    gwmask = 0
    for hna in self.hnalist:
      if hna.genmask > gwmask and hna.ip_in_net(addr):
        gwresult = hna.gateway
        mask = hna.genmask
    return gwresult

  def getMainAddress(self, addr):
    if self.aliasdict.has_key(addr):
      return addr
    for mainaddr, aliases in self.aliasdict.iteritems():
      for alias in aliases:
        if alias == addr:
          return mainaddr
    # assume it is a main address with no aliases (i.e. the only OLSR IP address of the node)
    return addr

  def __loadG(self, u_source, u_destination):
    self.G = nx.DiGraph()
    self.G.add_weighted_edges_from([(link.lastHopIP, link.destinationIP, 1 / (link.linkQuality * link.neighborLinkQuality)) for link in self.linklist])
    #G.add_weighted_edges_from([(link.lastHopIP, link.destinationIP, link.tcEdgeCost) for link in self.linklist])

    source = self.getMainAddress(u_source)
    if source == u_source:
      source = self.getHnaGateway(u_source)
      if source != u_source:
        printout( "Source %s is in an HNA. Using %s for path computation." % (u_source, source))
        self.G.add_weighted_edges_from([(u_source, source, 0)])
        source = u_source

    destination = self.getMainAddress(u_destination)
    if destination == u_destination:
      destination = self.getHnaGateway(u_destination)
      if destination != u_destination:
        printout( "Destination %s is in an HNA. Using %s for path computation." % (u_destination, destination))
        self.G.add_weighted_edges_from([(destination, u_destination, 0)])
        destination = u_destination

    return (source, destination)

  def get_etx(self, u_source, u_destination):
    source, destination = self.__loadG(u_source, u_destination)

    if source in self.G.nodes() and destination in self.G.nodes():
      return nx.dijkstra_path_length(self.G, source, destination)
    elif source in self.G.nodes():
      # find the closest gateway
      closestgw = None
      cost = 0
      for gw in self.gatewaylist:
        splen = nx.shortest_path_length(self.G, source, gw)
        if splen > cost:
          cost = splen
          closestgw = gw
      if closestgw:
        printout( "Warning: using gateway %s" % (closestgw,))
        return nx.dijkstra_path_length(self.G, source, closestgw)
      else:
        return 1.0
    else:
      return 1.0

  def get_shortest_path(self, u_source, u_destination):
    source, destination = self.__loadG(u_source, u_destination)

    if source in self.G.nodes() and destination in self.G.nodes():
      return nx.dijkstra_path(self.G, source, destination)
    elif source in self.G.nodes():
      # find the closest gateway
      closestgw = None
      cost = 0
      for gw in self.gatewaylist:
        splen = nx.shortest_path_length(self.G, source, gw)
        if splen > cost:
          cost = splen
          closestgw = gw
      if closestgw:
        printout( "Warning: using gateway %s" % (closestgw,))
        return nx.dijkstra_path(self.G, source, closestgw)
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
        path = t.get_shortest_path(src, dst)
        if path == None or len(path) < 1:
                printout( "No path found. Please check the script parameters")
                sys.exit(2)
        previoushop = None
        for hop in path:
          if previoushop != None:
              print "%.3f\t" % t.get_etx(previoushop, hop),
          else:
              print "\t",

          print hop,
          aliases = t.getAliases(hop)
          if len(aliases) < 1:
            print ""
          else:
            print "\t (" + ", ".join(aliases) + ")"

          previoushop = hop


