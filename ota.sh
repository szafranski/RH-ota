#!/bin/bash

##################
### fun stuff
dots7() { # done that way so it work on every terminal
  for _ in {1..7}; do
    printf "."
    sleep 0.2
  done
  printf "\n"
}

##################
check_package() {
  if dpkg-query -l "$1" >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi

}

check_python_package() {
  if python3 -c "import $1" >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

echo "dependencies will be auto-detected and installed"
echo "installing dependencies may need 'sudo' password"

which python3 >/dev/null
if [ $? -gt 0 ]; then
  echo python3 has to be installed && sudo apt install python3 -y
else
  echo python3"           "found # those  cure my ocd
fi

which avrdude >/dev/null
if [ $? -gt 0 ]; then
  echo avrdude has to be installed && sudo apt install avrdude -y
else
  echo avrdude"           "found
fi

which curl >/dev/null
if [ $? -gt 0 ]; then
  echo curl has to be installed && sudo apt install curl -y
else
  echo curl"              "found
fi

which cowsay >/dev/null
if [ $? -gt 0 ]; then
  echo cowsay has to be installed && sudo apt install cowsay -y
else
  echo cowsay"            "found
fi

which pip3 >/dev/null
if [ $? -gt 0 ]; then
  echo pip3 package has to be installed && sudo apt install python3-pip -y
else
  echo pip3"              "found
fi

if check_package 'python3-gpiozero'; then
  echo python3-gpiozero"  "found
else
  echo python3-gpiozero has to be installed && sudo apt install python3-gpiozero -y
fi

if check_package 'python3-requests'; then
  echo python3-requests"  "found
else
  echo python3-requests has to be installed && sudo apt install python3-requests -y
fi

if check_package 'python3-dev'; then
  echo python3-dev"       "found
else
  echo python3-dev has to be installed && sudo apt install python3-dev -y
fi

if check_package 'fonts-symbola'; then
  echo fonts-symbola"     "found
else
  echo fonts-symbola has to be installed && sudo apt install fonts-symbola -y
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

if check_package 'i2c-tools'; then
  echo i2c-tools"         "found
else
  echo i2c-tools has to be installed && sudo apt install i2c-tools -y
fi

if check_python_package 'RPi.GPIO'; then
  echo python3-rpi.gpio"  "found
else
  echo python3-rpi.gpio has to be installed && pip3 install rpi.gpio || echo - only on Pi -
fi

if check_python_package 'smbus'; then
  echo python3-smbus"     "found
else
  echo python3-smbus has to be installed && pip3 install smbus
fi

python3 start_ota.py
