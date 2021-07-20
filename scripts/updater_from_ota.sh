#!/bin/bash

dots50() {
  for _ in {1..50}; do
    printf "."
    sleep 0.05
  done
  printf "\n\n"
}

green="\033[92m"
endc="\033[0m"
underline="\033[4m"

printf "\n\nSoftware will be automatically closed.\n"
printf "\nWord 'Killed' may be shown.\n"
printf "\nPlease wait...\n"
sleep 1.2
printf "\n\nEnter 'sudo' password if prompted.\n"
sleep 1.2
sudo echo
printf "\n\nUpdating process has been started\n\n" &
dots50
printf "\n"
for pid in $(pgrep -ax python3 | grep start_ota.py | awk '{print $1}'); do kill -9 "$pid"; done
cd ~ || exit
rm -rf ~/.ota_markers/old_RH-ota >/dev/null 2>&1
cp -r ~/RH-ota ~/.ota_markers/old_RH-ota
cd ~/.ota_markers/old_RH-ota || exit
python3 ~/.ota_markers/old_RH-ota/self_update.py
cd ~ || exit
sleep 1.2
cd ~/RH-ota || exit
printf "\n\n $green Update process done, please "$underline"re-enter$endc$green ~/RH-ota directory \n"
printf "  by typing$endc 'cd ~/RH-ota'$green or just type$endc 'ota'\n"
printf "\n\n"
printf "         -- Hit Enter to continue --"
printf "\n\n"
