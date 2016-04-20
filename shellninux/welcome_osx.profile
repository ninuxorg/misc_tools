export TERM="xterm-color"

## -------------------------
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
UserName="${USER}"
host_name="${HOSTNAME}"
distro_ver="$(sw_vers -productName) $(sw_vers -productVersion)"
up_time="$( uptime | cut -d ',' -f1 | cut -d ' ' -f4-6 )"
CPU_Arch="$(uname -m)"
ip4_eth="$(ifconfig | grep -o -E '([[:xdigit:]]{1,3}\.){3}[[:xdigit:]]{1,3}' | grep -v "255" | grep -v "127.0.0" | tr -s '\n' ' ' )"
ip4_wan="$(curl --silent http://www.tzunami.it/IP.php)"
ip6_lan="$(ifconfig | grep -o -E '([[:xdigit:]]{1,4}\:){7}[[:xdigit:]]{1,4}' | grep "2001" | tr -s '\n' ' ')"
## ----------------------------------------------------------
echo
echo -e "        Welcome user:[${C_WHITE} ${UserName} ${C_DEFAULT}]"
echo -e "  You are on machine:[${C_RED} ${host_name} ${C_DEFAULT}]"
echo -e "    CPU architecture:[${C_BROWN} ${CPU_Arch} ${C_DEFAULT}]"
echo -e "      Running Distro:[${C_GREEN} ${distro_ver} ${C_DEFAULT}]"
echo -e "         With UpTime:[${C_CYAN} ${up_time} ${C_DEFAULT}]"
echo -e "Your private IPv4 is:[${C_YELLOW} ${ip4_eth}${C_DEFAULT}]"
echo -e " Your public IPv4 is:[${C_YELLOW} ${ip4_wan} ${C_DEFAULT}]"
echo -e "your IPv6 address is:[${C_BLUE} ${ip6_lan}${C_DEFAULT}]"
tput sgr0   # Reset attributes.
echo

PS1="\[${C_LIGHTGREEN}\]\u@\h\[${C_LIGHTBLUE}\]\w\$\[${C_DEFAULT}\] "
