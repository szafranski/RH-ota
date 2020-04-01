#!/bin/bash

sleep 2
avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/pi/"${1}".hex:i
echo
echo   ------ node flashed ------
echo


# backup flashing script - instruction:
# push reset pins of all nodes - and keep them pushed
# open script: 'sh ./flash.sh node_master' or 'sh ./flash.sh node_stable'
# when some text shows on terminal window
# release the button on the node that you want to flash
# you may release all buttons after you see "node flashed" info