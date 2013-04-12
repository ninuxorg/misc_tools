#!/bin/bash
#
# EASY IP LOGGER
#
mkdir /var/log/IP_CHECK
touch /var/log/IP_CHECK/ip.log
DIR="/var/log/IP_CHECK/ip.log"

while true; do
echo -e "\n#################### [$(date +"\033[01;32m%F\033[00m \033[01;31m%T\033[00m")] ######################" >> $DIR
test_ping=$(ping -c 3 www.google.com | while read pong; do echo -e "[$(date +"\033[01;32m%F\033[00m \033[01;31m%T\033[00m")] ${pong}"; done)
test_ip=$(curl -s checkip.dyndns.com | awk ' BEGIN { FS = ": " } ; {print $2} ' | cut -d '<' -f1 | while read ip; do echo -e "[$(date +"\033[01;32m%F\033[00m \033[01;31m%T\033[00m")] ${ip}"; done)
echo -e "${test_ping}\n" >> $DIR
echo "${test_ip}" >> $DIR
echo -e "#################################################################\n" >> $DIR
sleep 60
done
exit 0
