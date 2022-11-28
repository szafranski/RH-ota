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

print_info_message() {
  printf "dependencies will be auto-detected and installed \n"
  printf "installing dependencies may need 'sudo' password\n\n"
}

check_for_new_ota() {

  if ! test -f .first_time_here; then
    wget https://raw.githubusercontent.com/szafranski/RH-ota/stable/version.txt -q -O .new_ota_version_check_file.txt
    diff version.txt .new_ota_version_check_file.txt > .new_ota_version_diff_file
  else
    sudo apt update || printf "repositories have not been updated \n"
  fi
}

open_software_alias_check() {

  if ! grep -q "alias ota=" ../.bashrc; then
    echo '
#[added during RH-OTA setup]
alias ota="cd ~/RH-ota && sh ./ota.sh"                        # opens OTA software' >> ../.bashrc
  fi

  if ! grep -q "alias rh=" ../.bashrc; then
    echo '
#[added during RH-OTA setup]
alias rh="cd ~/RotorHazard/src/server && python3 server.py"   # starts RH-server' >> ../.bashrc
  fi
}

dependencies_check() {

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

  which procps >/dev/null
  if [ $? -gt 0 ]; then
    echo procps has to be installed && sudo apt install procps -y
  else
    echo procps"              "found
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

}

print_info_message
check_for_new_ota
open_software_alias_check &
dependencies_check &
wait
python3 start_ota.py
