#!/bin/bash
# $1 is linux user name
# $2 is actual version of RotorHazard to get.

warning_show(){
  echo "

  Installing additional software may take few minuts

"
}

sudo apt-get update && sudo apt-get upgrade -y
sudo apt autoremove -y
sudo apt install wget python2.7 ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus build-essential python-pip python-rpi.gpio git scons swig zip -y
sudo -H pip install cffi pillow
cd /home/"${1}" || exit
if [ -d "/home/${1}/RotorHazard" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard" "/home/${1}/RotorHazard_$(date +%Y%m%d%H%M)" || exit 1
fi
if [ -d "/home/${1}/RotorHazard-${2}" ]; then
  # Control will enter here if $DIRECTORY exists.
  mv "/home/${1}/RotorHazard-${2}" "/home/${1}/RotorHazard_${2}_$(date +%Y%m%d%H%M)" || exit 1
fi
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"${2}" -O temp.zip
unzip temp.zip
rm temp.zip
mv /home/"${1}"/RotorHazard-"${2}" /home/"${1}"/RotorHazard || exit 1
warning_show
sudo -H pip install -r /home/"${1}"/RotorHazard/src/server/requirements.txt
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
cd /home/"${1}" || exit
sudo git clone https://github.com/jgarff/rpi_ws281x.git
cd /home/"${1}"/rpi_ws281x || exit
warning_show
sudo scons
cd /home/"${1}"/rpi_ws281x/python || exit
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/chrisb2/pi_ina219.git
cd /home/"${1}"/pi_ina219 || exit
warning_show
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/rm-hull/bme280.git
cd /home/"${1}"/bme280 || exit
warning_show
sudo python setup.py install
sudo apt-get install openjdk-8-jdk-headless -y
sudo rm /lib/systemd/system/rotorhazard.service > /dev/null 2>&1
echo
echo "
[Unit]
Description=RotorHazard Server
After=multi-user.target

[Service]
WorkingDirectory=/home/${1}/RotorHazard/src/server
ExecStart=/usr/bin/python server.py

[Install]
WantedBy=multi-user.target
" | sudo tee -a /lib/systemd/system/rotorhazard.service
echo
sudo chmod 644 /lib/systemd/system/rotorhazard.service
sudo systemctl daemon-reload
sudo systemctl enable rotorhazard.service
echo
