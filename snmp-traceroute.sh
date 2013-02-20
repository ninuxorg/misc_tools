#!/bin/sh
# SNMP-TRACEROUTE: This script performs a traceroute showing IP, device_name and contact_name for each hop
#   Copyleft - all rights reversed - 2012 LuX@ninux.org
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ChangeLog
#   Ver.: 1.1 [2012-12-02]
#   - fixed: now the first hop shows localhost info, instead of waiting for the timeout.
#   - added: minor aesthetic improvements.

EXPECTED_ARGS=1 # Number of arguments expected.
E_BADARGS=85    # Exit value if incorrect number of args passed.

test $# -ne ${EXPECTED_ARGS} && echo "Usage: `basename $0` IPv4" && exit ${E_BADARGS}

# Track dependencies
E_BADEPENDS=90  # Exit value if unmet dependencies.
ErrorMsg=""
SnmpWalk=$(which snmpwalk)      || ErrorMsg="snmpwalk";
Tail=$(which tail)              || ErrorMsg="tail";
Awk=$(which awk)                || ErrorMsg="awk";
Sed=$(which sed)                || ErrorMsg="sed";
Echo=$(which echo)              || ErrorMsg="echo";
TraceRoute=$(which traceroute)  || ErrorMsg="traceroute";

if [ ! -z "${ErrorMsg}" ] ; then
        echo "Command not found: ${ErrorMsg}"
        exit ${E_BADEPENDS}
fi

${Echo} "IPv4		HostName		Contact"

${TraceRoute} -n ${1} 2>/dev/null | while read TraceRow; do
        IPv4=$( ${Echo} "${TraceRow}" | ${Sed} 's/to/127.0.0.1/g' | ${Awk} '{print $2}' | ${Sed} 's/*//g' )
        ${Echo} -n "${IPv4}	"
        HostName=$( ${SnmpWalk} -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.5.0 2>/dev/null | ${Awk} '{print $4}' | ${Sed} 's/\"//g' )
	${Echo} -n "${HostName}		"
	Contact=$( ${SnmpWalk} -v 1 -c public ${IPv4} 1.3.6.1.2.1.1.4.0 2>/dev/null | ${Awk} 'BEGIN { FS = ":" } ; { print $2 }' | ${Sed} 's/\"//g' )
        ${Echo} "${Contact}"
done

exit 0
