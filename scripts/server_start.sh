#!/bin/bash

dots5() { # done that way so it work on every terminal
  for _ in {1..5}; do
    printf "."
    sleep 0.4
  done
  printf "\n\n"
}

error_handling(){
  echo "

  Error - trying to start the server again...

  "
  python server.py ;
  echo "

LOOKS LIKE ERROR OCCURRED

Please try:
manually enabling I2C interface with 'sudo raspi-config'
manually changing RH directory permissions with 'sudo chmod -R 777 ~/RotorHazard'
"
read -p "Hit Enter when done " var
}

printf "You can stop the server by pressing Ctrl+C "
printf "Server booting, please wait"
dots5
echo
cd ~/RotorHazard/src/server || exit
python2.7 server.py || error_handling

# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.

# shellcheck disable=SC2034

# reload_ota() #  doesn't work
# {
# kill -9 $(pidof python3 update.py)
# python3 update.py
# }
