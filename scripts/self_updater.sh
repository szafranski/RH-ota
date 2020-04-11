#!/bin/bash

cd ~ || exit
rm -rf ~/RH-ota*
rm tempota.zip >/dev/null >/dev/null 2>&1
wget https://codeload.github.com/szafranski/RH-ota/zip/"${1}" -O tempota.zip
unzip tempota.zip
rm tempota.zip
mv RH-ota-* RH-ota
rm ~/wget* > /dev/null 2>&1
