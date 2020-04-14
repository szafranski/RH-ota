#!/bin/bash

warning_show(){
  echo "

  Installing additional software may take few minuts

"
}

sudo -H python -m pip install --upgrade pip
sudo -H pip install pillow
sudo apt-get install libjpeg-dev ntp -y
sudo apt-get update && sudo apt-get upgrade -y
sudo apt autoremove -y
upgradeDate="$(date +%Y%m%d%H%M)"
cd /home/"${1}" || exit
if [ -d "/home/${1}/RotorHazard" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard" "/home/${1}/RotorHazard_${upgradeDate}" || exit 1
fi
if [ -d "/home/${1}/RotorHazard-${2}" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard-${2}" "/home/${1}/RotorHazard_${2}_${upgradeDate}" || exit 1
fi
sudo rm -r /home/"${1}"/temp.zip >/dev/null 2>&1           # just in case of weird sys config
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"${2}" -O temp.zip
unzip temp.zip
rm ~/wget* > /dev/null 2>&1
mv /home/"${1}"/RotorHazard-"${2}" /home/"${1}"/RotorHazard
sudo rm temp.zip
sudo mkdir /home/"${1}"/backup_RH_data >/dev/null 2>&1
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
sudo chmod 777 -R /home/"${1}"/RotorHazard_"${upgradeDate}"
sudo chmod 777 -R /home/"${1}"/backup_RH_data
sudo chmod 777 -R /home/"${1}"/.ota_markers
sudo chmod 777 -R ~/RotorHazard
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/image /home/"${1}"/backup_RH_data
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/image /home/"${1}"/RotorHazard/src/server/static
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cd /home/"${1}"/RotorHazard/src/server || exit
warning_show
sudo pip install --upgrade --no-cache-dir -r requirements.txt

