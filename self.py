from time import sleep
import os
import sys
#import json

if os.path.exists("~/RH-ota/updater-config.json") == True:
	config_file_exists = True

if config_file_exists == True:
	os.system("sudo cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
os.system("sudo rm -r ~/RH-ota")
os.system("git clone --depth=1 https://github.com/szafranski/RH-ota.git") 
if config_file_exists == True:
	os.system("sudo cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
print("\n\n\n\t\t RotorHazard OTA Manager updated - you can see 'update-notes.txt'\n\n\n")
sleep(2)


