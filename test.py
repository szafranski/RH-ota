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
	f = open(homedir+"/.ota_markers/.version","r")
	for line in f:
		global version_name
		version_name=line
versionCheck()

print(version_name)
