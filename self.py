from time import sleep
import os
import sys
import json

os.system("pwd >.my_pwd")
with open('.my_pwd', 'r') as file:
	myhomedir = file.read().replace('\n', '')

cfgdir1= str(myhomedir+'/RH-ota/updater-config.json')
cfgdir2= str(myhomedir+'/RH-ota/distr-updater-config.json')

if os.path.exists(myhomedir+"/RH-ota/updater-config.json") == True:
	with open(cfgdir1) as config_file:
		data = json.load(config_file)
else:
	with open(cfgdir2) as config_file:
		data = json.load(config_file)

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

if os.path.exists(cfgdir1) == True:
	config_file_exists = True
	if data['debug_mode'] == 1:
		linux_testing = True
	else:
		linux_testing = False 
	if linux_testing == True:
		user = data['debug_user']
	else:
		user = data['pi_user']
else:
	config_file_exists = False

if config_file_exists == True:
	if check_if_string_in_file(myhomedir+'/RH-ota/updater-config.json', 'updates_without_pdf'):
		if data['updates_without_pdf'] == 1:
			no_pdf_update = True
		else:
			pdf_update = False 
	else:
		pdf_update = True

def oldVersionCheck():
	os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.old_version")
	os.system("sed -i 's/updater_version = //' ~/.ota_markers/.old_version")
	os.system("sed -i 's/#.*/ /' ~/.ota_markers/.old_version")
	f = open(""+myhomedir+"/.ota_markers/.old_version","r")
	for line in f:
		global old_version_name
		old_version_name = line

def newVersionCheck():
	os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.new_version")
	os.system("sed -i 's/updater_version = //' ~/.ota_markers/.new_version")
	os.system("sed -i 's/#.*/ /' ~/.ota_markers/.new_version")
	f = open(""+myhomedir+"/.ota_markers/.new_version","r")
	for line in f:
		global new_version_name
		new_version_name = line

def main():
	os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")   ### resolves compatibility issues
	os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")         ### resolves compatibility issues
	oldVersionCheck()
	print("\n\n\n\t Please wait: updating process from version "+old_version_name+"\n\n")
	if config_file_exists == True:
		os.system("cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
	# if pdf_update == True:
	os.system("sudo rm -r ~/RH-ota")
	os.system("git clone --depth=1 https://github.com/szafranski/RH-ota.git")
	# else:
		# os.system("sudo rm -r ~/RH-ota")
		# os.system("git clone -b no_pdf --depth=1 https://github.com/szafranski/RH-ota.git")
	if config_file_exists == True:
		os.system("cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
	newVersionCheck()
	print("\n\n\n\t RotorHazard OTA Manager updated to version "+new_version_name+"\n\t\tYou may check update-notes.txt\n\n")
	sleep(1.5)
main()
