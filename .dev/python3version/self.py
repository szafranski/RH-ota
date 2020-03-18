from time import sleep
import os
import sys
import json
import time

os.system("pwd >.my_pwd")
with open('.my_pwd', 'r') as file:
    myhomedir = file.read().replace('\n', '')
os.system("rm ./.my_pwd")

cfgdir1= str(myhomedir+'/RH-ota/updater-config.json')
cfgdir2= str(myhomedir+'/RH-ota/distr-updater-config.json')

def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False

if os.path.exists(myhomedir+"/RH-ota/updater-config.json") == True:
    with open(cfgdir1) as config_file:
        data = json.load(config_file)
else:
    with open(cfgdir2) as config_file:
        data = json.load(config_file)

def internetCheck():
    print("\nPlease wait - checking internet connection state...\n")
    global internet_FLAG
    before_millis = int(round(time.time() * 1000))
    os.system(". "+myhomedir+"/RH-ota/open_scripts.sh; net_check")
    #os.system("timeout 3s sh "+myhomedir+"/RH-ota/net_check.sh > /dev/null 2>&1")
    while True:
        now_millis = int(round(time.time() * 1000))
        time_passed = (now_millis - before_millis)
        if os.path.exists("./index.html") == True:
            internet_FLAG=1
            break
        elif (time_passed > 10100):
            internet_FLAG=0
            break
    os.system("rm "+myhomedir+"/RH-ota/index.html > /dev/null 2>&1")
    os.system("rm "+myhomedir+"/RH-ota/wget-log* > /dev/null 2>&1")
    os.system("rm "+myhomedir+"/index.html > /dev/null 2>&1")
    os.system("rm "+myhomedir+"/wget-log* > /dev/null 2>&1")

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
            no_pdf_update = False
    else:
        no_pdf_update = False
else: 
    no_pdf_update = False

def debugInfo():
    if config_file_exists == True:
        print("config_file_exists = True")
    else:
        print("config_file_exists = False")
    if no_pdf_update == True:
        print("no_pdf_update = True")
    else:
        print("no_pdf_update = False")
    sleep(1)
#debugInfo()

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
    internetCheck()
    if internet_FLAG==0:
        print("\nLooks like you don't have internet connection. Update canceled.")
        sleep(2)
    else:
        print("\nInternet connection - OK")
        sleep(1.5)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")   ### resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")         ### resolves compatibility issues
        oldVersionCheck()
        print("\n\n\n\t Please wait: updating process from version "+old_version_name+"\n\n")
        sleep(2)
        if config_file_exists == True:
            os.system("cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
        if no_pdf_update == False:
            print("Update will contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        else:
            print("Update won't contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/no_pdf_included -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        if config_file_exists == True:
            os.system("cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
        newVersionCheck()
        print("\n\n\n\t RotorHazard OTA Manager updated to version "+new_version_name+"\n\t\tYou may check update-notes.\n\n")
        sleep(1)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")   ### resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")         ### resolves compatibility issues
main()