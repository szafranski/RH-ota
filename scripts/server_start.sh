#!/bin/bash

dots5() { # done that way so it work on every terminal
  for _ in {1..5}; do
    printf "."
    sleep 0.4
  done
  printf "\n\n"
}

error_handling() {
  echo "

  Error - trying to start the server with sudo...

  "
  sudo python3 server.py

  echo "

LOOKS LIKE ERROR OCCURRED

You may want to try:
- manually enable I2C interface with 'sudo raspi-config'
- manually change RH directory permissions with 'sudo chmod -R 777 ~/RotorHazard'
- if you see 'sqlalchemy.exc.OperiationalError' you may try to remove old 'database.db'
file from '~/RotorHazard/src/server/' directory and attempt to restart the server then

-- If you just stopped the server with a keyboard (Ctrl+C) - ignore that message --

"
  read -p "Hit Enter to exit now " var
}

echo "You can stop the server by pressing Ctrl+C "
printf "Server booting, please wait"
dots5
echo
cd ~/RotorHazard/src/server || exit
python3 server.py || error_handling

# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.

# shellcheck disable=SC2034

# reload_ota() #  doesn't work
# {
# kill -9 $(pidof python3 update.py)
# python3 update.py
# }
