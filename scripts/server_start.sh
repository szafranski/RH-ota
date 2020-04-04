#!/bin/bash

dots5() { # done that way so it work on every terminal
  for i in {1 2 3 4 5}; do
    printf "."
    sleep 0.4
  done
  printf "\n\n"
}

printf "Server booting, please wait"
dots5
cd ~/RotorHazard/src/server || exit
python server.py

# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.

# shellcheck disable=SC2034

# reload_ota() #  doesn't work
# {
# kill -9 $(pidof python3 update.py)
# python3 update.py
# }
