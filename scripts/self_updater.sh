#!/bin/bash

sudo rm -rf ~/RH-ota*
wget https://codeload.github.com/szafranski/RH-ota/zip/"${1}" -O tempota.zip
rm tempota.zip >/dev/null >/dev/null 2>&1
unzip tempota.zip
rm tempota.zip
mv RH-ota-* RH-ota
