#!/bin/bash
EXPECTED_ARGS=1 # Number of arguments expected.
E_BADARGS=85    # Exit value if incorrect number of args passed.
test $# -ne ${EXPECTED_ARGS} && echo "Usage: `basename $0` IPv4" && exit ${E_BADARGS}
echo "It may take time. Please wait.."
ElencoHopDuplicati=$( traceroute -n ${1} 2>/dev/null | tail -n +2 | awk '{print $2}' | sed 's/*//g' | sort -n | uniq -d )
echo "IPv4      HostName        Contact"
for IPv4 in ${ElencoHopDuplicati}; do
        NomeHost=$( snmpwalk -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.5.0 2>/dev/null | awk '{print $4}' )
        Contatto=$( snmpwalk -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.4.0 2>/dev/null | awk '{print $4}' )
        echo "${IPv4}   ${NomeHost}     ${Contatto}"
done
exit 0
