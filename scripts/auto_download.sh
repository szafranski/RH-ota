#!/bin/bash


green="\033[92m"
red="\033[91m"
endc="\033[0m"


script(){
(sudo apt update && sudo apt install curl wget unzip -y) || echo "no wget or curl download target"
cd ~ || return 1
mv RH-ota* RH-ota.old >> /dev/null 2&>1           #TODO in case of non-empty directories
mv tempota.zip tempota.zip.old >> /dev/null 2&>1  #TODO in case of non-empty directories
wget https://codeload.github.com/szafranski/RH-ota/zip/main -O tempota.zip || return 1
unzip tempota.zip || return 1
rm tempota.zip || return 1
mv RH-ota-* RH-ota || return 1

printf "
$green
Program downloaded successfully. To open the program now type:
$endc
cd ~/RH-ota
./ota.sh

"

}

script || printf "
$red
errors encountered - try manual installation -> more info od github
$endc

"

