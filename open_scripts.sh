#!/bin/bash

reload_ota() #  doesn't work
{
kill -9 $(pidof python3 update.py)
python3 update.py
}

dots5()
{
for i in {1..5};
do
printf "."
sleep 0.5
done
printf "\n\n"
}

dots30()
{
for i in {1..30};
do
printf "."
sleep 0.08
done
printf "\n\n"
}

server_start () 
{
printf "Server booting, please wait"
dots5
cd ~/RotorHazard/src/server
python server.py
}

rh_configuration_start()
{
cd ~/RH-ota
python3 ./conf_wizard_rh.py
}

ota_configuration_start()
{
cd ~/RH-ota
python3 ./conf_wizard_ota.py
}

updater_from_ota()
{
printf "\n\nSoftware will be automatically closed.\n"
printf "\nWord 'Killed' may be shown.\n"
sleep 1.2
printf "\n\nEnter 'sudo' password if prompted.\n"
sleep 1.2
sudo echo
printf "\n\nUpdating process has been started\n\n"
dots30
kill -9 $(pidof python3 update.py)
cd ~
cp ~/RH-ota/self.py ~/.ota_markers/self.py 
python3 ~/.ota_markers/self.py
cd ~
sleep 1.2
cd ~/RH-ota
printf "\n\nUpdate completed, hit 'Enter' to continue \n\n"
}

# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.

