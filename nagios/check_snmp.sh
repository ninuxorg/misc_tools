#!/bin/bash 
# -h IP -C community -o OID -w WARNING_THRESHOLD -c CRITICAL_THRESHOLD 
IP=
COMMUNITY=
OID=
WARNING_THRESHOLD=
CRITICAL_THRESHOLD=
while getopts "h:C:o:w:c:" OPTION
do
     case $OPTION in
      h)
       IP=$OPTARG 
       ;;
      C)
       COMMUNITY=$OPTARG
       ;;
      o)
       OID=$OPTARG
       ;;
      w)
       WARNING_THRESHOLD=$OPTARG
       ;;
      c)
       CRITICAL_THRESHOLD=$OPTARG
       ;;
     esac
done
# echo $IP $COMMUNITY $OID $WARNING_THRESHOLD $CRITICAL_THRESHOLD 
RES=$(snmpget -c $COMMUNITY -v1 $IP -On $OID | cut -d " " -f 4)

echo "Actual OID value:" $RES

if [ $RES -lt $WARNING_THRESHOLD ]; then
    exit 0
elif [ $RES -lt $CRITICAL_THRESHOLD ]; then
    exit 1
else
    exit 2
fi


# CPU = .1.3.6.1.4.1.10002.1.1.1.4.2.1.3.1
# snmpwalk -c public -v1 $1 -On .1.3.6.1.4.1.14988.1.1.1.2.1.3 | awk -F"." '{for(i=15;i<20;i++)printf("%lx:",$i); printf("%lx ",$20); print $NF}' | awk '{print $1,$NF}'

