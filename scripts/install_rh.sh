#!/bin/bash
# $1 is linux user name
# $2 is actual version of RotorHazard to get.

warning_show() {
  echo "

  Installing additional software may take few minuts

"
}

sudo apt-get update && sudo apt-get --with-new-pkgs upgrade -y
sudo apt autoremove -y
sudo apt install wget python3 ntp htop libjpeg-dev libffi-dev build-essential git scons swig zip i2c-tools python3-smbus python3-pip python3-dev -y
sudo apt install python-rpi.gpio || echo "-- no python-rpi.gpio module found - available only on Pi --"  #to be checked
sudo apt install python3-rpi.gpio || echo "-- no python-rpi.gpio module found - available only on Pi --" #is this redundant?
sudo -H pip3 install cffi pillow
sudo -H python3 -m pip install --upgrade pip
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
rm ~/wget* >/dev/null 2>&1
mv /home/"${1}"/RotorHazard-"${2}" /home/"${1}"/RotorHazard || exit 1
warning_show
sudo -H pip3 install -r /home/"${1}"/RotorHazard/src/server/requirements.txt
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
cd /home/"${1}" || exit
sudo git clone https://github.com/jgarff/rpi_ws281x.git
cd /home/"${1}"/rpi_ws281x || exit
warning_show
sudo scons
cd /home/"${1}"/rpi_ws281x/python || exit
sudo python3 setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/chrisb2/pi_ina219.git
cd /home/"${1}"/pi_ina219 || exit
warning_show
sudo python3 setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/rm-hull/bme280.git
cd /home/"${1}"/bme280 || exit
warning_show
sudo python3 setup.py install
sudo apt-get install openjdk-11-jdk-headless -y
sudo rm /lib/systemd/system/rotorhazard.service >/dev/null 2>&1
echo
echo "
[Unit]
Description=RotorHazard Server
After=multi-user.target

[Service]
WorkingDirectory=/home/${1}/RotorHazard/src/server
ExecStart=/usr/bin/python3 server.py

[Install]
WantedBy=multi-user.target
" | sudo tee -a /lib/systemd/system/rotorhazard.service
echo
sudo chmod 644 /lib/systemd/system/rotorhazard.service
sudo systemctl daemon-reload
sudo systemctl enable rotorhazard.service
echo

sudo cp /etc/rc.local /etc/rc.local.save_iptables
sudo sed -i 's/exit 0//' /etc/rc.local

# port forwarding
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save

echo "
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save

exit 0
" | sudo tee -a /etc/rc.local

echo "

port forwarding added

"