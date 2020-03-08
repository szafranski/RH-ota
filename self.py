from time import sleep
import os
import sys

homedir = os.path.expanduser('~')

if os.path.exists(homedir+"/RH-ota/updater-config.json") == True:
	config_file_exists = True
else:
	config_file_exists = False

def oldVersionCheck():
	os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.old_version")
	os.system("sed -i 's/updater_version = //' ~/.ota_markers/.old_version")
	os.system("sed -i 's/#.*/ /' ~/.ota_markers/.old_version")
	f = open(homedir+"/.ota_markers/.old_version","r")
	for line in f:
		global old_version_name
		old_version_name = line

def newVersionCheck():
	os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.new_version")
	os.system("sed -i 's/updater_version = //' ~/.ota_markers/.new_version")
	os.system("sed -i 's/#.*/ /' ~/.ota_markers/.new_version")
	f = open(homedir+"/.ota_markers/.new_version","r")
	for line in f:
		global new_version_name
		new_version_name = line

def main():
	oldVersionCheck()
	print("\n\n\n\t Please wait: updating process from version "+old_version_name+"\n\n")
	if config_file_exists == True:
		os.system("cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
	os.system("rm -r ~/RH-ota -y")
	os.system("git clone --depth=1 https://github.com/szafranski/RH-ota.git") 
	if config_file_exists == True:
		os.system("cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
	newVersionCheck()
	print("\n\n\n\t RotorHazard OTA Manager updated to version "+new_version_name+"\n\t\tYou may check update-notes.txt\n\n")
	sleep(1.5)
main()

