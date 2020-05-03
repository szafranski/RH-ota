#!/bin/bash

sleep 2
echo
avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"${1}"/node_firmware.hex:i
echo
echo   ------ node flashed ------
echo


# backup flashing script - instruction:
# insert your desired firmware hex into pi home directory
# change its name to node_firmware.hex
# push reset pins of all nodes - and keep them pushed
# open script: 'sh ./flash.sh <username>' like: 'sh ./flash.sh pi'
# when some text shows on terminal window
# release the button on the node that you want to flash
# you may release all buttons after you see "node flashed" info