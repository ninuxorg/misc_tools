#!/bin/bash
echo Maytake long time
EXPECTED_ARGS=1 # Number of arguments expected.
E_BADARGS=85    # Exit value if incorrect number of args passed.
test $# -ne ${EXPECTED_ARGS} && echo "Usage: `basename $0` IPv4" && exit ${E_BADARGS}
ElencoHop=$( traceroute -n ${1} 2>/dev/null | tail -n +2 | awk '{print $2}' )
for IPv4 in ${ElencoHop}; do
       HostName=$( snmpget -v1 -c public ${IPv4} sysName.0 2>/dev/null | awk '{print $4}' )
       echo "${IPv4}   ${HostName}"
done
exit 0
