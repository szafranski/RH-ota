#!/bin/bash

which python3 >/dev/null
if [ $? -gt 0 ]; then
  echo python3 has to be installed && sudo apt install python3
else
  echo python3 '\t' found # those '\t' cure my ocd
fi

which avrdude >/dev/null
if [ $? -gt 0 ]; then
  echo avrdude has to be installed && sudo apt install avrdude
else
  echo avrdude '\t' found
fi

which curl >/dev/null
if [ $? -gt 0 ]; then
  echo curl has to be installed && sudo apt install curl
else
  echo curl '\t''\t' found
fi

which cowsay >/dev/null
if [ $? -gt 0 ]; then
  echo cowsay has to be installed && sudo apt install cowsay
else
  echo cowsay '\t''\t' found
fi

which pip3 >/dev/null
if [ $? -gt 0 ]; then
  echo pip3 package has to be installed && sudo apt install python3-pip
else
  echo pip3 '\t''\t' found
fi

# "looking for dependencies python..."

pip3 freeze >pip3installed.tmp

# "looking for non python dependencies..."
#sudo apt list 2>/dev/null | tee aptinstalled.tmp >/dev/null # I removed 'sudo' so it won't ask for admin pswd always
apt list 2>/dev/null | tee aptinstalled.tmp >/dev/null

if grep -q 'python3-gpiozero' aptinstalled.tmp; then
  echo python3-gpiozero '\t' found
else
  echo echo python3-gpiozero has to be installed && sudo apt install python3-gpiozero
fi

if grep -q 'python3-dev' aptinstalled.tmp; then
  echo python3-dev '\t' found
else
  echo echo python3-dev has to be installed && sudo apt install python3-dev
fi

if grep -q 'python3-rpi.gpio' aptinstalled.tmp; then
  echo python3-rpi.gpio '\t' found
else
  echo echo python3-rpi.gpio has to be installed && sudo apt install python3-rpi.gpio
fi

if grep -q 'python3-smbus' aptinstalled.tmp; then
  echo python3-smbus '\t' found
else
  echo echo python3-smbus has to be installed && sudo apt install python3-smbus
fi

if grep -q 'emoji' aptinstalled.tmp; then
  echo python3-smbus '\t' found
else
  echo echo emoji has to be installed && sudo pip install emoji
fi

if grep -q 'i2c-tools' aptinstalled.tmp; then
  echo i2c-tools '\t' found
else
  echo echo i2c-tools has to be installed && sudo apt install python3-smbus
fi

if grep -q 'zip' aptinstalled.tmp; then
  echo zip '\t' found
else
  echo echo zip has to be installed && sudo apt install zip unzip # todo does it check for unzip too?
fi

# Cleanup after myself.
rm pip3installed.tmp
rm aptinstalled.tmp

python3 update.py

# todo 'sudo -H' with pip should be used? yellow prompts are showing

# shellcheck disable=SC2230
