#!/bin/bash

script(){
cd ~ || return 1
wget https://codeload.github.com/szafranski/RH-ota/zip/stable -O tempota.zip || return 1
unzip tempota.zip || return 1
rm tempota.zip || return 1
mv RH-ota-* RH-ota || return 1
cd RH-ota || return 1

echo "

Program downloaded successfully. To open the program now type:

cd RH-ota
./ota.sh

"

}

script || echo "

errors encountered - try manual installation -> more info od github

"

