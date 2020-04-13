#!/bin/bash

dots50() {
  for i in {1..50}; do
    printf "."
    sleep 0.05
  done
  printf "\n\n"
}

printf "\n\nSoftware will be automatically closed.\n"
printf "\nWord 'Killed' may be shown.\n"
sleep 1.2
printf "\n\nEnter 'sudo' password if prompted.\n"
sleep 1.2
sudo echo
printf "\n\nUpdating process has been started\n\n" & dots50
printf "\n"
# todo not always kills properly more than one instance:
for pid in $(pgrep -ax python3 | grep update.py | awk '{print $1}' ) ; do kill -9 $pid ; done
cd ~ || exit
rm -rf ~/.ota_markers/old_RH-ota > /dev/null 2>&1
cp -r ~/RH-ota ~/.ota_markers/old_RH-ota
cd ~/.ota_markers/old_RH-ota || exit
python3 ~/.ota_markers/old_RH-ota/self.py
cd ~ || exit
sleep 1.2
cd ~/RH-ota || exit
printf "\n\nUpdate process done, please re-enter ~/RH-ota folder \n\n"
printf "\n\n"
printf "         -- Hit Enter to continue --"
printf "\n\n"
