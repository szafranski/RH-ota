#!/bin/bash

printf "Server booting, please wait"
dots5()
{
for i in {1..5};
do
printf "."
sleep 0.5
done
printf "\n\n"
}
dots5
cd ~/RotorHazard/src/server || exit
python server.py


# scripts like those ensures that files are being executed in right directory but main program
# istelf can be continued from previous directory after such a script was executed or stopped
# eg. after hitting Ctrl+C after server was started etc.


# reload_ota() #  doesn't work
# {
# kill -9 $(pidof python3 update.py)
# python3 update.py
# }
