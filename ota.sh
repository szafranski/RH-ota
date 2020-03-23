#!/bin/bash

#printf "\nchecking python3 installation\n\n"

which python3 > /dev/null
if [ $? -gt 0 ]; 
	then echo python3 has to be installed && sudo apt install python3
fi;

which python3-gpiozero > /dev/null
if [ $? -gt 0 ];
	then echo python3-gpio has to be installed && sudo apt install python3-gpiozero
fi;

which avrdude > /dev/null
if [ $? -gt 0 ];
	then echo cowsay has to be installed && sudo apt install avrdude
fi;

which cowsay > /dev/null
if [ $? -gt 0 ];
	then echo cowsay has to be installed && sudo apt install python3-gpio
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
sudo apt list  2>/dev/null | tee aptinstalled.tmp  >/dev/null

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
#Cleanup after myself.
rm pip3installed.tmp
rm aptinstalled.tmp

python3 update.py


# todo David - ota everytime asks for sudo - only on debug or always?
# todo are all echoes necesarry?
# todo 'sudo -H' with pip should be used? yellow prompts are showing