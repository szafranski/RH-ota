#!/bin/bash

dots30() {
  for i in {1..30}; do
    printf "."
    sleep 0.08
  done
  printf "\n\n"
}

printf "\n\nSoftware will be automatically closed.\n"
printf "\nWord 'Killed' may be shown.\n"
sleep 1.2
printf "\n\nEnter 'sudo' password if prompted.\n"
sleep 1.2
sudo echo
printf "\n\nUpdating process has been started\n\n" & dots30
kill -9 "$(pidof python3 update.py)"
# todo:
# 1. right now it kills ALL python3 processes, not just update.py - bad
# 2. kill multiple instances of 'python3 update.py' if needed
cd ~ || exit
rm -rf ~/.ota_markers/old_RH-ota > /dev/null 2>&1
cp -r ~/RH-ota ~/.ota_markers/old_RH-ota
cd ~/.ota_markers/old_RH-ota || exit
python3 ~/.ota_markers/old_RH-ota/self.py
cd ~ || exit
sleep 1.2
cd ~/RH-ota || exit
printf "\n\nUpdate process done, hit 'Enter' to continue \n\n"
cd ~ || exit
# todo exit to home folder - now it "ends" in RH-ota