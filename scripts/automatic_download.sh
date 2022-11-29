#!/bin/bash

cd ~
wget https://codeload.github.com/szafranski/RH-ota/zip/stable -O tempota.zip
unzip tempota.zip
rm tempota.zip
mv RH-ota-* RH-ota
