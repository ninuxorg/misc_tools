wget -q -O - http://IP_DELLA_MACCHINA_OLSR:2006/hna | grep "/0" | sort -n | awk '{print $2}' | while read ip_add; do snmpwalk -v1 -c public ${ip_add} iso.3.6.1.2.1.1.5.0 | awk '{print $4}' | while read ip_name; do echo -e "${ip_add} ${ip_name}"; done; done


