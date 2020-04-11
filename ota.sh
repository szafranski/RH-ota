#!/bin/bash

##################
### fun stuff
dots7() { # done that way so it work on every terminal
for i in {1 2 3 4 5 6 7}; do
  printf "."
  sleep 0.2
done
printf "\n"
}
###############
echo dependencies will be auto-detected and installed
echo installing dependencies may need 'sudo' password

which python3 >/dev/null
if [ $? -gt 0 ]; then
  echo python3 has to be installed && sudo apt install python3 -y
else
  echo python3"    "found # those  cure my ocd
fi

which avrdude >/dev/null
if [ $? -gt 0 ]; then
  echo avrdude has to be installed && sudo apt install avrdude -y
else
  echo avrdude"    "found
fi

which curl >/dev/null
if [ $? -gt 0 ]; then
  echo curl has to be installed && sudo apt install curl -y
else
  echo curl"       "found
fi

which cowsay >/dev/null
if [ $? -gt 0 ]; then
  echo cowsay has to be installed && sudo apt install cowsay -y
else
  echo cowsay"     "found
fi

which pip3 >/dev/null
if [ $? -gt 0 ]; then
  echo pip3 package has to be installed && sudo apt install python3-pip -y
else
  echo pip3"       "found
fi

echo looking for dependencies
echo please wait

dots7 & pip3 freeze >pip3installed.tmp

dots7 & apt list 2>/dev/null | tee aptinstalled.tmp >/dev/null

if grep -q 'python3-gpiozero' aptinstalled.tmp; then
  echo python3-gpiozero" "found
else
  echo python3-gpiozero has to be installed && sudo apt install python3-gpiozero -y
fi

if grep -q 'python3-requests' aptinstalled.tmp; then
  echo python3-requests" "found
else
  echo python3-requests has to be installed && sudo apt install python3-requests -y
fi

if grep -q 'python3-dev' aptinstalled.tmp; then
  echo python3-dev"      "found
else
  echo python3-dev has to be installed && sudo apt install python3-dev -y
fi

#if grep -q 'twemoji-svginot' aptinstalled.tmp; then
#  echo fonts-twemoji"    "found
#else
#  echo fonts-symbola has to be installed &&
#  sudo apt-get install software-properties-common -y &&
#  sudo apt-add-repository ppa:eosrei/fonts -y &&
#  sudo apt-get update &&
#  sudo apt-get install fonts-twemoji-svginot -y
#fi

if grep -q 'i2c-tools' aptinstalled.tmp; then
  echo i2c-tools"        "found
else
  echo i2c-tools has to be installed && sudo apt install i2c-tools -y
fi

if grep -q 'RPi.GPIO' pip3installed.tmp; then
  echo python3-rpi.gpio" "found
else
  echo python3-rpi.gpio has to be installed && pip3 install rpi.gpio || echo - only on Pi -
fi

if grep -q 'smbus' pip3installed.tmp; then
  echo python3-smbus"    "found
else
  echo python3-smbus has to be installed && pip3 install smbus
fi

# Cleanup after myself.
rm pip3installed.tmp
rm aptinstalled.tmp

python3 update.py

# shellcheck disable=SC2230
# due to 'which' reporting
