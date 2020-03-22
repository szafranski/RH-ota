#!/bin/bash

#printf "\nchecking python3 installation\n\n"

which python3 > /dev/null
if [ $? -gt 0 ]; 
	then echo python3 has to be installed && sudo apt install python3
fi;

which pip3 > /dev/null  # proper way of checking?
if [ $? -gt 0 ];
	then echo pip package has to be installed && sudo apt install python3-pip
fi;
echo "looking for dependencies python ..."
pip3 freeze > pip3installed.tmp

if grep -q 'configparser' pip3installed.tmp ; then
  echo configparser installed
else
  echo configparser has to be installed && sudo pip3 install configparser
fi

echo "looking for non python dependencies..."
sudo apt list | tee aptinstalled.tmp > /dev/null

if grep -q 'python3-dev' aptinstalled.tmp ; then
  echo python3-dev installed
else
  echo echo python3-dev has to be installed && sudo apt install python3-dev
fi

if grep -q 'python3-rpi.gpio' aptinstalled.tmp ; then
  echo python3-rpi.gpio installed
else
  echo echo python3-rpi.gpio has to be installed && sudo apt install python3-rpi.gpio
fi

if grep -q 'python3-smbus' aptinstalled.tmp ; then
  echo python3-smbus installed
else
  echo echo python3-smbus has to be installed && sudo apt install python3-smbus
fi


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


