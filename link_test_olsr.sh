#!/bin/bash
# USAGE sh ./link_test_olsr.sh IP_DEL_GATEWAY_OLSR
# Sequenze escape dei colori
C_WHITE='\033[1;37m'
C_LIGHTGRAY='\033[0;37m'
C_GRAY='\033[1;30m'
C_BLACK='\033[0;30m'
C_RED='\033[0;31m'
C_LIGHTRED='\033[1;31m'
C_GREEN='\033[0;32m'
C_LIGHTGREEN='\033[1;32m'
C_BROWN='\033[0;33m'
C_YELLOW='\033[1;33m'
C_BLUE='\033[0;34m'
C_LIGHTBLUE='\033[1;34m'
C_PURPLE='\033[0;35m'
C_PINK='\033[1;35m'
C_CYAN='\033[0;36m'
C_LIGHTCYAN='\033[1;36m'
C_DEFAULT='\033[0m'
## -------------------------

EXPECTED_ARGS=1 # Number of arguments expected.
E_BADARGS=85    # Exit value if incorrect number of args passed.

test $# -ne ${EXPECTED_ARGS} && echo "Usage: `basename $0` IPv4" && exit ${E_BADARGS}

# Track dependencies
E_BADEPENDS=90  # Exit value if unmet dependencies.
ErrorMsg=""
Wget=$(which wget)              || ErrorMsg="wget";
Sed=$(which sed)                || ErrorMsg="sed";
Echo=$(which echo)              || ErrorMsg="echo";
Awk=$(which awk)                || ErrorMsg="awk";
Grep=$(which grep)              || ErrorMsg="grep";
Sort=$(which sort)              || ErrorMsg="sorti";
Uniq=$(which uniq)              || ErrorMsg="uniq";
Egrep=$(which egrep)            || ErrorMsg="egrep";

if [ ! -z "${ErrorMsg}" ] ; then
        echo "Command not found: ${ErrorMsg}"
        exit ${E_BADEPENDS}
fi

${Echo} -e "${C_WHITE}STA IP\t\tAP IP\t\tHyst.\tLQ\tNLQ\tCost${C_DEFAULT}"

${Wget} -q -O - http://${1}:2006/topo | ${Awk} '{print $1}' | ${Grep} "172.1" | ${Sort} -n | ${Uniq} 2>/dev/null | while read Topo_v4; do
	${Wget} -q -O - http://${Topo_v4}:2006/link | ${Egrep} -e '172.1|192.168|10.' | ${Sort} -n | ${Sed} -e 's/[^0-9]*$//' 2>/dev/null | while read Link_v4; do
		${Wget} -q -O - http://${Topo_v4}:2007/link >/dev/null 2>&1 && TEST_V6=1 || TEST_V6=0
		[ ${TEST_V6} -eq 1 ] && Link_v6=$( ${Wget} -q -O - http://${Topo_v4}:2007/link | grep "2001:" )
		Remote_IP=$( ${Echo} "${Link_v4}" | ${Awk} '{print $2}' )
		Test_class=$( ${Echo} "${Remote_IP}" | ${Grep} -v "172.1" | ${Awk} 'BEGIN { FS = "." } ; { print $1 }' )
		if [ -z ${Test_class} ]
			then
				${Echo} -e "${C_CYAN}${Link_v4}\n${Lan}" | ${Sed} -e '/^$/d'
				${Echo} -e "${C_PURPLE}${Link_v6}${C_DEFAULT}" | ${Sed} -e '/^$/d'
			else
				Lan=$( ${Echo} -e "${C_YELLOW}${Link_v4}" )
		fi
	done
done
exit 0

