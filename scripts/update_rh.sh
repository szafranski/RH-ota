#!/bin/bash

sudo -H python -m pip install --upgrade pip
sudo -H pip install pillow 
sudo apt-get install libjpeg-dev ntp -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt autoremove -y
sudo mkdir /home/"${1}"/.old_RotorHazard.old  >/dev/null 2>&1
sudo cp -r /home/"${1}"/RotorHazard-* /home/"${1}"/.old_RotorHazard.old/ >/dev/null 2>&1
sudo rm -r /home/"${1}"/RotorHazard-master >/dev/null 2>&1  # just in case of weird sys cfg
sudo rm -r /home/"${1}"/temp.zip >/dev/null 2>&1  # just in case of weird sys config
sudo cp -r /home/"${1}"/RotorHazard.old /home/"${1}"/.old_RotorHazard.old/ >/dev/null 2>&1
sudo rm -r /home/"${1}"/RotorHazard.old >/dev/null 2>&1
sudo mv /home/"${1}"/RotorHazard /home/"${1}"/RotorHazard.old
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/${2} -O temp.zip
unzip temp.zip
mv /home/"${1}"/RotorHazard-${2} /home/"${1}"/RotorHazard
sudo rm temp.zip
sudo mkdir /home/"${1}"/backup_RH_data >/dev/null 2>&1
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
sudo chmod 777 -R /home/"${1}"/RotorHazard.old
sudo chmod 777 -R /home/"${1}"/.old_RotorHazard.old
sudo chmod 777 -R /home/"${1}"/backup_RH_data
sudo chmod 777 -R /home/"${1}"/.ota_markers
cp /home/"${1}"/RotorHazard.old/src/server/config.json /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp -r /home/"${1}"/RotorHazard.old/src/server/static/image /home/"${1}"/backup_RH_data
cp -r /home/"${1}"/RotorHazard.old/src/server/static/image /home/"${1}"/RotorHazard/src/server/static
cp /home/"${1}"/RotorHazard.old/src/server/config.json /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard.old/src/server/database.db /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard.old/src/server/database.db /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cd /home/"${1}"/RotorHazard/src/server || exit
sudo pip install --upgrade --no-cache-dir -r requirements.txt