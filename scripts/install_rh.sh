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
warning_show()
sudo -H pip install -r /home/"${1}"/RotorHazard/src/server/requirements.txt
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
cd /home/"${1}" || exit
sudo git clone https://github.com/jgarff/rpi_ws281x.git
cd /home/"${1}"/rpi_ws281x || exit
warning_show()
sudo scons
cd /home/"${1}"/rpi_ws281x/python || exit
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/chrisb2/pi_ina219.git
cd /home/"${1}"/pi_ina219 || exit
warning_show()
sudo python setup.py install
cd /home/"${1}" || exit
sudo git clone https://github.com/rm-hull/bme280.git
cd /home/"${1}"/bme280 || exit
warning_show()
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
sudo chmod 777 -R ~/RotorHazard
echo

# todo below is a source of that script - may be deleted after testing
# os.system("sudo apt-get update && sudo apt-get upgrade -y")
# os.system("sudo apt autoremove -y")
# os.system("sudo apt install wget ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus \
# build-essential python-pip git scons swig zip -y")
# if linux_testing:  # on Linux PC system
#     os.system("sudo apt dist-upgrade -y")
# else:  # on Raspberry
#     os.system("sudo apt install python-rpi.gpio")
#     if conf_allowed:
#         sys_conf()
# os.system("sudo -H pip install cffi pillow")
# os.chdir("/home/" + user)
# if not os.path.exists(f"/home/{user}/.old_RotorHazard.old"):
#     os.system(f"mkdir /home/{user}/.old_RotorHazard.old")
# if os.path.exists(f"/home/{user}/RotorHazard"):
#     os.system(f"cp -r /home/{user}/RotorHazard /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
#     #  in case of forced installation
#     os.system(f"rm -r /home/{user}/RotorHazard >/dev/null 2>&1")  # in case of forced installation
# os.system(f"rm /home/{user}/temp >/dev/null 2>&1")  # in case of forced installation
# os.system(f"cp -r /home/{user}/RotorHazard-* /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
# # in case of forced installation
# os.system(f"rm -r /home/{user}/RotorHazard-* >/dev/null 2>&1")  # in case of forced installation
# os.chdir(f"/home/{user}")
# os.system(f"wget https://codeload.github.com/RotorHazard/RotorHazard/zip/{server_version} -O temp.zip")
# os.system("unzip temp.zip")
# os.system("rm temp.zip")
# os.system(f"mv /home/{user}/RotorHazard-{server_version} /home/{user}/RotorHazard")
# os.system(f"sudo -H pip install -r /home/{user}/RotorHazard/src/server/requirements.txt")
# os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard/src/server")
# os.chdir(f"/home/{user}")
# os.system("sudo git clone https://github.com/jgarff/rpi_ws281x.git")
# os.chdir(f"/home/{user}/rpi_ws281x")
# os.system("sudo scons")
# os.chdir(f"/home/{user}/rpi_ws281x/python")
# os.system("sudo python setup.py install")
# os.chdir(f"/home/{user}")
# os.system("sudo git clone https://github.com/chrisb2/pi_ina219.git")
# os.chdir(f"/home/{user}/pi_ina219")
# os.system("sudo python setup.py install")
# os.chdir(f"/home/{user}")
# os.system("sudo git clone https://github.com/rm-hull/bme280.git")
# os.chdir(f"/home/{user}/bme280")
# os.system("sudo python setup.py install")
# config_soft['rh_installation_done'] = 1
# json.dump()  # soft config
# os.system("sudo apt-get install openjdk-8-jdk-headless -y")
# os.system("sudo rm /lib/systemd/system/rotorhazard.service")
# os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system(f"echo 'WorkingDirectory=/home/{user}/RotorHazard/src/server' \
# | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
# os.system("sudo chmod 644 /lib/systemd/system/rotorhazard.service")
# os.system("sudo systemctl daemon-reload")
# os.system("sudo systemctl enable rotorhazard.service")
