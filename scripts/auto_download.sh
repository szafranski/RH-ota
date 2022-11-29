#!/bin/bash


green="\033[92m"
red="\033[91m"
endc="\033[0m"


script(){
cd ~ || return 1
wget https://codeload.github.com/szafranski/RH-ota/zip/stable -O tempota.zip || return 1
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

