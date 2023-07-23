#!/bin/bash

cd ~ || exit
rm -rf ~/RH_Install-Manager*
rm tempota.zip >/dev/null >/dev/null 2>&1
wget https://codeload.github.com/RotorHazard/Install-Manager/zip/"${1}" -O tempota.zip
unzip tempota.zip
rm tempota.zip
mv RH_Install-Manager-* RH_Install-Manager
rm ~/wget* >/dev/null 2>&1
