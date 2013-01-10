#!/bin/sh

# Released under the GPLv3 Licence
#
# @AUTHORS: Clauz (clauz@ninux.org), Hispanico (marco.giuntini@gmail.com), Stefano (stefano@ninux.org)
# 

IP_PING=78.47.48.238 #Address to check for ADSL Connection
ADSL_GW='192.168.1.254' #Address of the ADSL Gateway
RT_TABLE=detection_table #Name of the new routing table for ADSL gw malfunction detection
RT_TABLE_NUM=201 #Number of the routing table for ADSL gw malfunction detection

(grep $RT_TABLE /etc/iproute2/rt_tables >/dev/null) || (echo $RT_TABLE_NUM $RT_TABLE >> /etc/iproute2/rt_tables)
(ip r s table $RT_TABLE |grep -F $ADSL_GW >/dev/null) || (ip route add table $RT_TABLE default via $ADSL_GW) 

(ip rule show |grep -F $IP_PING >/dev/null) || (ip rule add to $IP_PING table $RT_TABLE pref 500) 

while [ 1 ]; do
		if ping -q -c 1 $IP_PING >/dev/null 2>/dev/null; then
			(ip r s |grep -F $ADSL_GW >/dev/null) || (ip route add default via $ADSL_GW && /etc/init.d/olsrd restart)
		else
			(ip r s |grep -F $ADSL_GW >/dev/null) && (ip route del default via $ADSL_GW && /etc/init.d/olsrd restart)
		fi
		sleep 50
done

