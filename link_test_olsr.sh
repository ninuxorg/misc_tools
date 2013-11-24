#!/bin/bash
# Version Beta 2.0
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
Tr=$(which tr)                  || ErrorMsg="tr";

if [ ! -z "${ErrorMsg}" ] ; then
        echo "Command not found: ${ErrorMsg}"
        exit ${E_BADEPENDS}
fi

${Echo} -e "${C_WHITE}STA IP\t\tAP IP\t\tHyst.\tLQ\tNLQ\tCost${C_DEFAULT}"

${Wget} -q -O - http://${1}:2006/topo | ${Awk} '{print $1}' | ${Grep} "172.1" | ${Sort} -n | ${Uniq} 2>/dev/null | while read Topo_v4; do
	${Wget} -q -O - http://${Topo_v4}:2006/link | ${Egrep} -e '172.1|192.168|10.' | ${Sort} -n | ${Sed} -e 's/[^0-9]*$//' 2>/dev/null | while read Link_v4; do
		${Wget} -q -O - http://${Topo_v4}:2007/link >/dev/null 2>&1 && TEST_V6=1 || TEST_V6=0
		[ ${TEST_V6} -eq 1 ] && Link_v6L=$( ${Wget} -q -O - http://${Topo_v4}:2007/link | ${Grep} -v "2001:4c00:893b:1:" | ${Sed} -e 's/[^0-9]*$//' ) && Link_v6W=$( ${Wget} -q -O - http://${Topo_v4}:2007/link | ${Grep} "2001:4c00:893b:1:" )
		Local_IP4=$( ${Echo} "${Link_v4}" | ${Grep} "172.1" | ${Awk} '{print $1}' )
		Local_IP6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $1}' | ${Tr} -s '\n' ' ' )
		Local_IP6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $1}' )
		Remote_IP4=$( ${Echo} "${Link_v4}" | ${Awk} '{print $2}' )
		Remote_IP6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $2}' | ${Tr} -s '\n' ' ' )
		Remote_IP6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $2}' )
		Hyst4=$( ${Echo} "${Link_v4}" | ${Awk} '{print $3}' )
		Hyst6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $3}' | ${Tr} -s '\n' ' ' )
		Hyst6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $3}' )
		LQ4=$( ${Echo} "${Link_v4}" | ${Awk} '{print $4}' )
		LQ6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $4}' | ${Tr} -s '\n' ' ' )
		LQ6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $4}' )
		NLQ4=$( ${Echo} "${Link_v4}" | ${Awk} '{print $5}' )
		NLQ6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $5}' | ${Tr} -s '\n' ' ' )
		NLQ6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $5}' )
		Cost4=$( ${Echo} "${Link_v4}" | ${Awk} '{print $6}' )
		Cost6L=$( ${Echo} -e "${Link_v6L}" | ${Awk} '{print $6}' | ${Tr} -s '\n' ' ' )
		Cost6W=$( ${Echo} "${Link_v6W}" | ${Awk} '{print $6}' )
		Test_class4=$( ${Echo} "${Remote_IP4}" | ${Grep} -v "172.1" | ${Awk} 'BEGIN { FS = "." } ; { print $1 }' )
		if [ -z ${Test_class4} ]
			then
				IP4W=$( ${Echo} -e "${C_CYAN}${Local_IP4}\t${Remote_IP4}\t${Hyst4}\t${LQ4}\t${NLQ4}\t${Cost4}\n${IP4L}" | ${Sed} -e '/^$/d' )
				IP6W=$( ${Echo} -e "${C_PURPLE}${Local_IP6W}\t${Remote_IP6W}\t${Hyst6W}\t${LQ6W}\t${NLQ6W}\t${Cost6W}${C_DEFAULT}" )
			else
				IP4L=$( ${Echo} -e "${C_YELLOW}${Link_v4}${C_DEFAULT}" )
				IP6L=$( ${Echo} -e "${C_PURPLE}${Local_IP6L}\t${Remote_IP6L}\t${Hyst6L}\t${LQ6L}\t${NLQ6L}\t${Cost6L}${C_DEFAULT}" )
				
		fi
		${Echo} -e "${IP4W}\n${IP6W}\n${IP6L}" | ${Sed} -e '/^$/d'
	done
done
exit 0

