#!/bin/bash

if [ $# -lt 2 ]; then
		echo "Usage: $0 <partition to check> <alert treshold>"
		exit 1
fi

ADMIN="zioproto@gmail.com"
ALERT=$2
check_part=$1

df -H  > /tmp/df.out
cat /tmp/df.out | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do

  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  
  if [ $partition = $check_part ]; then
  	if [ $usep -ge $ALERT ]; then
    		echo "Fine dello spazio \"$partition ($usep%)\" su $(hostname) il $(date)" | mail -a "From: script check space" -s Space-Central Server $ADMIN
  	fi
  fi
done
