#!/bin/sh

EXPECTED_ARGS=1 # Number of arguments expected.
E_BADARGS=85    # Exit value if incorrect number of args passed.
test $# -ne ${EXPECTED_ARGS} && echo "Usage: `basename $0` IPv4" && exit ${E_BADARGS}

# Track dependencies
E_BADEPENDS=90  # Exit value if unmet dependencies.
ErrorMsg=""
SnmpWalk=$(which snmpwalk)    	|| ErrorMsg="snmpwalk";
Tail=$(which tail)            	|| ErrorMsg="tail";
Awk=$(which awk)              	|| ErrorMsg="awk";
Sed=$(which sed)              	|| ErrorMsg="sed";
Echo=$(which echo)            	|| ErrorMsg="echo";
TraceRoute=$(which traceroute)	|| ErrorMsg="traceroute";

if [ ! -z "${ErrorMsg}" ] ; then
	echo "Command not found: ${ErrorMsg}"
	exit ${E_BADEPENDS}
fi

${Echo} "IPv4			HostName			Contact"

${TraceRoute} -n ${1} 2>/dev/null | while read TraceRow; do 
	IPv4=$( ${Echo} "${TraceRow}" | ${Awk} '{print $2}' | ${Sed} 's/*//g' )
	${Echo} -n "${IPv4}		"
	HostName=$( ${SnmpWalk} -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.5.0 2>/dev/null | ${Awk} '{print $4}' )
	Contact=$( ${SnmpWalk} -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.4.0 2>/dev/null | ${Awk} '{print $4}' )
	${Echo} "${HostName}			${Contact}" 
done

exit 0
