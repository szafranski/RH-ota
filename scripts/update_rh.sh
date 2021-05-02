#!/bin/bash

time_warning_show() {
  echo "


      Installing additional software may take few minutes

"
}

sudo -H python3 -m pip install --upgrade pip
sudo -H pip3 install pillow
sudo apt-get install libjpeg-dev ntp htop -y
sudo apt-get update && sudo apt-get --with-new-pkgs upgrade -y
sudo apt autoremove -y
sudo chmod -R 777 "/home/${1}/RotorHazard" # to ensure smooth operation if files in RH directory were edited etc. and permissions changed
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
sudo rm -r /home/"${1}"/temp.zip >/dev/null 2>&1 # just in case of weird sys config
cd /home/"${1}" || exit
wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"${2}" -O temp.zip
unzip temp.zip
rm ~/wget* >/dev/null 2>&1
mv /home/"${1}"/RotorHazard-"${2}" /home/"${1}"/RotorHazard
sudo rm temp.zip
sudo mkdir /home/"${1}"/backup_RH_data >/dev/null 2>&1
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
sudo chmod 777 -R /home/"${1}"/RotorHazard_"${upgradeDate}"
sudo chmod 777 -R /home/"${1}"/backup_RH_data
sudo chmod 777 -R /home/"${1}"/.ota_markers
sudo chmod 777 -R ~/RotorHazard
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static /home/"${1}"/backup_RH_data
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/user/* /home/"${1}"/RotorHazard/src/server/static/user/ || printf "\n no user folder found in this RotorHazard version - skipping \n" #rh_pr
mkdir /home/"${1}"/RotorHazard/src/server/db_bkp
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/db_bkp/* /home/"${1}"/RotorHazard/src/server/db_bkp/ || printf "\n no backup folder found in this RotorHazard version - skipping \n" #rh_pr
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/image /home/"${1}"/RotorHazard/src/server/static/image
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cd /home/"${1}"/RotorHazard/src/server || exit
time_warning_show
sudo pip3 install --upgrade --no-cache-dir -r requirements.txt

### python 3 transition handling ###

PYTHON3_CONVERSION_FLAG_FILE=/home/"${1}"/.ota_markers/python3_support_was_added

if ! test -f "$PYTHON3_CONVERSION_FLAG_FILE"; then

  SERVICE_FILE=/lib/systemd/system/rotorhazard.service
  old_python_service_statement="ExecStart=/usr/bin/python server.py"

  if test -f "$SERVICE_FILE"; then

    if grep -Fxq "$old_python_service_statement" "$SERVICE_FILE"; then
      printf "\n"
      echo "old python based RotorHazard autostart service found"
      sudo sed -i 's/python/python3/g' "$SERVICE_FILE"
      echo "changed to python3 based service"
    else
      echo "RotorHazard autostart service is up to date"
    fi
  else
    echo "no RotorHazard autostart service found - no changes"
  fi

  printf "\n"

  if grep -Fq "python server.py" "/home/"${1}"/.bashrc"; then
    echo "old python based server-start alias found"
    sed -i 's/python server.py/python3 server.py/g' ~/.bashrc
    echo "'ss' alias changed to python3 version"
  fi

  ### sensors transition to python3 handling ###

  printf "\n\n    Converting existing sensors libraries to python3 versions \n\n\n"

  INA_SENSOR_FILES=/home/"${1}"/pi_ina219

  if test -d "$INA_SENSOR_FILES"; then
    cd /home/"${1}" || exit
    sudo rm -r "$INA_SENSOR_FILES" || exit
    sudo git clone https://github.com/chrisb2/pi_ina219.git
    cd /home/"${1}"/pi_ina219 || exit
    printf "\n\n  INA sensor library will be updated to python3 \n\n"
    sudo python3 setup.py install
  fi

  BME_SENSOR_FILES=/home/"${1}"/bme280

  if test -d "$INA_SENSOR_FILES"; then
    cd /home/"${1}" || exit
    sudo rm -r "$BME_SENSOR_FILES" || exit
    sudo git clone https://github.com/rm-hull/bme280.git
    cd /home/"${1}"/bme280 || exit
    printf "\n\n  BME sensor library will be updated to python3 \n\n"
    sudo python3 setup.py install
  fi

  LEDS_LIBRARY_FILES=/home/"${1}"/rpi_ws281x

  if test -d "$LEDS_LIBRARY_FILES"; then
    cd /home/"${1}" || exit
    sudo rm -r "$LEDS_LIBRARY_FILES" || exit
    sudo git clone https://github.com/jgarff/rpi_ws281x.git
    cd /home/"${1}"/rpi_ws281x || exit
    printf "\n\n  LEDs controller library will be updated to python3  \n\n"
    sudo scons
    cd /home/"${1}"/rpi_ws281x/python || exit
    sudo python3 setup.py install
  fi

  touch "$PYTHON3_CONVERSION_FLAG_FILE"

  echo "


      supporting libraries updated to python3

"

fi

# port forwarding
if ! grep -q "sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000" /etc/rc.local; then

sudo cp /etc/rc.local /etc/rc.local.save_iptables

sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save


sudo sed -i 's/exit 0//' /etc/rc.local

echo "
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save
exit 0
" | sudo tee -a /etc/rc.local

echo "
port forwarding added - server available on port default 80
"
fi


cd /home/"${1}" || exit
