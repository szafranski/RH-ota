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
cd ~ || exit
rm -rf ~/.ota_markers/old_RH-ota > /dev/null 2>&1
cp -r ~/RH-ota ~/.ota_markers/old_RH-ota
cd ~/.ota_markers/old_RH-ota || exit
python3 ~/.ota_markers/old_RH-ota/self.py
cd ~ || exit
sleep 1.2
cd ~/RH-ota || exit
printf "\n\nUpdate completed, hit 'Enter' to continue \n\n"
