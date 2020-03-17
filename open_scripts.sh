#!/bin/bash

dots5()
{
for i in 1 2 3 4 5
do
printf "."
sleep 0.5
done
printf "\n\n"
}

dots30()
{
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
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

configuraton_start () 
{
cd ~/RH-ota
python ./conf_wizard_rh.py
}

net_check()
{
	rm index* > /dev/null 2>&1
#[ "$(ping -c 2 8.8.8.8 | grep '100% packet loss' )" != "" ]
timeout 10s wget www.google.com
#sleep 2
#exit
}

updater_from_ota()
{
printf "\n\nSoftware will be automatically closed.\n"
printf "\nWord 'Killed' may be shown.\n"
sleep 1.2
printf "\n\nEnter 'sudo' password if prompted.\n"
sleep 1.2
sudo echo
printf "\n\nUpdating process will be started soon.\n\n"
sleep 1
printf "\n\nUpdating process has been started\n\n"
dots30
kill -9 $(pidof python update.py)
cd ~
cp ~/RH-ota/self.py ~/.ota_markers/self.py 
python ~/.ota_markers/self.py
cd ~
cd ~/RH-ota
printf "\n\nUpdate completed, hit 'Enter' to continue \n\n"
}

log_me()
{
rm ./log.txt > /dev/null 2>&1
echo > ./log.txt
echo FILE /boot/config.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt
cat /boot/config.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt
echo FILE /boot/cmdline.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt
cat /boot/cmdline.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt
echo FILE updater-config.json | tee -a  ./log.txt
echo | tee -a  ./log.txt
cat ~/RH-ota/updater-config.json | tee -a  ./log.txt
echo | tee -a  ./log.txt
echo FILE ~/.ota_markers/ota_config.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt
cat ~/.ota_markers/ota_config.txt | tee -a  ./log.txt
echo | tee -a  ./log.txt

echo LOGGING TO FILE - DONE
sleep 1.5
}



# aliases_reload () 
# {
	# . ~/.bashrc
	# printf "aliases reloaded"
	# sleep 0.5
# }

# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.

