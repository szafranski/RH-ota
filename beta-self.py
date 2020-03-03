from time import sleep
import os
import sys
import json

with open('updater-config.json') as config_file:
	data = json.load(config_file)

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 
	
if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

os.chdir("/home/"+user)
if os.path.exists("/home/"+user+"/.ota_markers") == False:
	os.system("mkdir /home/"+user+"/.ota_markers")
if os.path.exists("/home/"+user+"/RH-ota") == True:
	os.system("sudo cp /home/"+user+"/RH-ota/updater-config.json /home/"+user+"/.ota_markers/updater-config.json")
	os.system("sudo rm -r /home/"+user+"/RH-ota")  
os.system("git clone -b updating_tests_and_net --depth=1 https://github.com/szafranski/RH-ota.git") 
os.system("sudo cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
print("\n\n\t\t RotorHazard OTA Manager updated - you can see update-notes.txt\n\n")
sleep(2)


