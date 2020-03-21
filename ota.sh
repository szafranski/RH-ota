#!/bin/bash

#printf "\nchecking python3 installation\n\n"

which python3 > /dev/null
if [ $? -gt 0 ]; 
	then echo python3 has to be installed && sudo apt install python3
fi;

#printf "\nchecking pip installation\n\n"

which pip3 > /dev/null  # proper way of checking?
if [ $? -gt 0 ]; 
	then echo pip package has to be installed && sudo apt install python3-pip
fi;

which python3-dev > /dev/null  # proper way of checking?
if [ $? -gt 0 ];
	then echo python3-dev has to be installed && sudo apt install python3-dev
fi;

which python3-rpi.gpio > /dev/null  # proper way of checking?
if [ $? -gt 0 ];
	then echo python3-rpi.gpio has to be installed && sudo apt install python3-rpi.gpio
fi;

which python3-smbus > /dev/null  # proper way of checking?
if [ $? -gt 0 ];
	then echo python3-smbus has to be installed && sudo apt install python3-smbus
fi;


#  todo has to be added for checking and pyhon3-pip is not being recognized - attempt to install every time


python3 update.py


#  old:

#python3_exists
# printf "Please enter 'sudo pswd'\n"
# sudo apt install python3
# sudo apt install python3-pip
# pip3 install configparser
# printf "\n"
# printf "Installation process completed. You may now open the software with a command 'python3 update.py'."
# printf "\n"
# sleep 1 
# python3 update.py


# Run this scripit with a command 'sh ./install.sh'.
# Next just open the software using simple 'python3 update.py'.
# Make sure that you have internet connection when installing.


