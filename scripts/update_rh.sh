#!/bin/bash

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
mv /home/"${1}"/RotorHazard-"${2}" /home/"${1}"/RotorHazard
sudo rm temp.zip
sudo mkdir /home/"${1}"/backup_RH_data >/dev/null 2>&1
sudo chmod 777 -R /home/"${1}"/RotorHazard/src/server
sudo chmod 777 -R /home/"${1}"/RotorHazard_${upgradeDate}
#sudo chmod 777 -R /home/"${1}"/.old_RotorHazard.old
sudo chmod 777 -R /home/"${1}"/backup_RH_data
sudo chmod 777 -R /home/"${1}"/.ota_markers
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/image /home/"${1}"/backup_RH_data
cp -r /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/static/image /home/"${1}"/RotorHazard/src/server/static
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/config.json /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/RotorHazard/src/server/ >/dev/null 2>&1 &
cp /home/"${1}"/RotorHazard_"${upgradeDate}"/src/server/database.db /home/"${1}"/backup_RH_data >/dev/null 2>&1 &
cd /home/"${1}"/RotorHazard/src/server || exit
sudo pip install --upgrade --no-cache-dir -r requirements.txt

# os.system("sudo -H python -m pip install --upgrade pip")
# os.system("sudo -H pip install pillow ")
# os.system("sudo apt-get install libjpeg-dev ntp -y")
# os.system("sudo apt-get update && sudo apt-get upgrade -y")
# if not linux_testing:
#     os.system("sudo apt dist-upgrade -y")
# os.system("sudo apt autoremove -y")
# if not os.path.exists(f"/home/{user}/.old_RotorHazard.old"):
#     os.system(f"sudo mkdir /home/{user}/.old_RotorHazard.old")
# os.system(f"sudo cp -r /home/{user}/RotorHazard-* /home/{user}/.old_RotorHazard.old/ >/dev/null 2>&1")
# os.system(f"sudo rm -r /home/{user}/RotorHazard-master >/dev/null 2>&1")  # just in case of weird sys cfg
# os.system(f"sudo rm -r /home/{user}/temp.zip >/dev/null 2>&1")  # just in case of weird sys config
# if os.path.exists(f"/home/{user}/RotorHazard.old"):
#     os.system(f"sudo cp -r /home/{user}/RotorHazard.old /home/{user}/.old_RotorHazard.old/")
#     os.system(f"sudo rm -r /home/{user}/RotorHazard.old")
# os.system(f"sudo mv /home/{user}/RotorHazard /home/{user}/RotorHazard.old")
# os.chdir(f"/home/{user}")
# os.system(f"wget https://codeload.github.com/RotorHazard/RotorHazard/zip/{server_version} -O temp.zip")
# os.system("unzip temp.zip")
# os.system(f"mv /home/{user}/RotorHazard-{server_version} /home/{user}/RotorHazard")
# os.system("sudo rm temp.zip")
# os.system(f"sudo mkdir /home/{user}/backup_RH_data >/dev/null 2>&1")
# os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard/src/server")
# os.system(f"sudo chmod 777 -R /home/{user}/RotorHazard.old")
# os.system(f"sudo chmod 777 -R /home/{user}/.old_RotorHazard.old")
# os.system(f"sudo chmod 777 -R /home/{user}/backup_RH_data")
# os.system(f"sudo chmod 777 -R /home/{user}/.ota_markers")
# os.system(f"cp /home/{user}/RotorHazard.old/src/server/config.json \
# /home/{user}/RotorHazard/src/server/ >/dev/null 2>&1 &")
# os.system(f"cp -r /home/{user}/RotorHazard.old/src/server/static/image \
# /home/{user}/backup_RH_data")
# os.system(f"cp -r /home/{user}/RotorHazard.old/src/server/static/image \
# /home/{user}/RotorHazard/src/server/static")
# os.system(f"cp /home/{user}/RotorHazard.old/src/server/config.json \
# /home/{user}/backup_RH_data >/dev/null 2>&1 &")
# os.system(f"cp /home/{user}/RotorHazard.old/src/server/database.db \
# /home/{user}/RotorHazard/src/server/ >/dev/null 2>&1 &")
# os.system(f"cp /home/{user}/RotorHazard.old/src/server/database.db \
# /home/{user}/backup_RH_data >/dev/null 2>&1 &")
# os.chdir(f"/home/{user}/RotorHazard/src/server")
# os.system("sudo pip install --upgrade --no-cache-dir -r requirements.txt")