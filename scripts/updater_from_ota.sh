#!/bin/bash

dots30()
{
for i in {1..30};
do
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
printf "\n\nUpdating process has been started\n\n"
dots30
kill -9 $(pidof python3 update.py)
cd ~ || exit
cp ~/RH-ota/self.py ~/.ota_markers/self.py 
python3 ~/.ota_markers/self.py
cd ~ || exit
sleep 1.2
cd ~/RH-ota || exit
printf "\n\nUpdate completed, hit 'Enter' to continue \n\n"

