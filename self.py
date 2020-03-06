from time import sleep
import os
import sys

homedir = os.path.expanduser('~')

if os.path.exists(homedir+"/RH-ota/updater-config.json") == True:
	config_file_exists = True
else:
	config_file_exists = False

def versionCheck():
	os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.version")
	os.system("sed -i 's/updater_version = / /' ~/.ota_markers/.version")
	os.system("sed -i 's/#.*/ /' ~/.ota_markers/.version")
	version_name=os.system("cat ~/.ota_markers/.version")

print("\n\n\n\t\t Updating process has been started...\n\n\n")
if config_file_exists == True:
	os.system("sudo cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
os.system("sudo rm -r ~/RH-ota")
os.system("git clone --depth=1 https://github.com/szafranski/RH-ota.git") 
if config_file_exists == True:
	os.system("sudo cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
versionCheck()
global version_name
print("\n\n\n\t\t RotorHazard OTA Manager updated to "+version_name+"- you can see 'update-notes.txt'\n\n\n")
sleep(2)


