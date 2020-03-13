#!/bin/bash

server_start () 
{
	printf "Server booting, please wait...\n\n"
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
timeout 3s wget www.google.com
#sleep 2
#exit
}

# aliases_reload () 
# {
	# . ~/.bashrc
	# printf "aliases reloaded"
	# sleep 0.5
# }

# script like this ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hittind Ctrl+C after server was started etc.
