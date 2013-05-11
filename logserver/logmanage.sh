#!/bin/bash
logdir="/var/log/"
fifodir="/var/log/"
# Name of logs
logname=(auth cron syslog)

# ---------------------------------------

if [[ $1 = "run" ]]; then
	echo "Creating Fifo"
	for logg in ${logname[@]}; do
		if [[ -p $fifodir$logg.fifo ]]; then
			echo "Removing and create fifo $fifodir$logg.fifo"
			rm $fifodir$logg.fifo
		else
			echo "Create fifo $fifodir$logg.fifo"
		fi
		mkfifo $fifodir$logg.fifo
	done

       for logg in ${logname[@]}; do
                if [[ -p $fifodir$logg.fifo ]]; then
			cat $fifodir$logg.fifo | while read LINE; do destination="$logdir$logg-$(echo $LINE| awk -F' ' '{print $4}').log"; echo $LINE | awk '{$4=""; print}' >> $destination; done &
		else
			echo "$fifodir$logg.fifo non trovata"		

		fi
	done
	exit 1

elif [[ $1 = "flush" ]]; then
	        echo "Flushing delle fifo"
       		for logg in ${logname[@]}; do
			if [[ -p $fifodir$logg.fifo ]]; then
				rm $fifodir$logg.fifo
			fi
		done
		exit 1
else
	echo "Usage:"
	echo "logmanage.sh run"
	echo "or"
	echo "logmanage.sh flush"

fi

