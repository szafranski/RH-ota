#!/bin/bash


green="\033[92m"
red="\033[91m"
endc="\033[0m"


script(){
(sudo apt update && sudo apt install curl wget unzip -y) || echo "no wget or curl download target"
cd ~ || return 1
mv RH_Install-Manager* RH_Install-Manager.old > /dev/null 2&>1           #TODO in case of non-empty directories
mv tempota.zip tempota.zip.old > /dev/null 2&>1  #TODO in case of non-empty directories
wget https://codeload.github.com/RotorHazard/Install-Manager/zip/stable -O tempota.zip || return 1
unzip tempota.zip || return 1
rm tempota.zip || return 1
mv RH_Install-Manager-* RH_Install-Manager || return 1

printf "
$green
Program downloaded successfully. To open the program now type:
$endc
cd ~/RH_Install-Manager
./rhim.sh

$yellow
For the NuclearHazard quick install, enter:
cd ~/RH_Install-Manager/NuclearHazard
./rh-install.sh 1
$endc
"

}

script || printf "
$red
errors encountered - try manual installation -> more info od GitHub
$endc

"

