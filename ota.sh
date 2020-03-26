#!/bin/bash

#printf "\nchecking python3 installation\n\n"

which python3 >/dev/null
if [ $? -gt 0 ]; then
  echo python3 has to be installed && sudo apt install python3
fi

which avrdude >/dev/null
if [ $? -gt 0 ]; then
  echo cowsay has to be installed && sudo apt install avrdude
fi

which curl >/dev/null
if [ $? -gt 0 ]; then
  echo curl has to be installed && sudo apt install curl
fi

which cowsay >/dev/null
if [ $? -gt 0 ]; then
  echo cowsay has to be installed && sudo apt install cowsay
fi

which pip3 >/dev/null # proper way of checking?
if [ $? -gt 0 ]; then
  echo pip package has to be installed && sudo apt install python3-pip
fi
echo "looking for dependencies python..."

pip3 freeze >pip3installed.tmp

echo "looking for non python dependencies..."
sudo apt list 2>/dev/null | tee aptinstalled.tmp >/dev/null

if grep -q 'python3-gpiozero' aptinstalled.tmp; then
  echo
#  echo python3-gpiozero installed
else
  echo echo python3-gpiozero has to be installed && sudo apt install python3-gpiozero
fi

if grep -q 'python3-dev' aptinstalled.tmp; then
  echo
#  echo python3-dev installed
else
  echo echo python3-dev has to be installed && sudo apt install python3-dev
fi

if grep -q 'python3-rpi.gpio' aptinstalled.tmp; then
  echo
#  echo python3-rpi.gpio installed
else
  echo echo python3-rpi.gpio has to be installed && sudo apt install python3-rpi.gpio
fi

if grep -q 'python3-smbus' aptinstalled.tmp; then
  echo
#  echo python3-smbus installed
else
  echo echo python3-smbus has to be installed && sudo apt install python3-smbus
fi

if grep -q 'i2c-tools' aptinstalled.tmp; then
  echo
#  echo i2c-tools installed
else
  echo echo i2c-tools has to be installed && sudo apt install python3-smbus
fi

#Cleanup after myself.
rm pip3installed.tmp
rm aptinstalled.tmp

python3 update.py

# todo 'sudo -H' with pip should be used? yellow prompts are showing
# todo check for python3-gpiozero, i2ctools and python3-rpi.gpio only on Pi
# not on any other 'platform'