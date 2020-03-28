from time import sleep
import os
import time
from modules import load_config, dots_show

config = load_config()

if config['debug_mode']:
    user = config['debug_user']
else:
    user = config['pi_user']

if config['updates_without_pdf']:
    no_pdf_update = True
else:
    no_pdf_update = False


if config['beta_tester']:
    beta_tester_update = True
else:
    beta_tester_update = False

if os.path.exists(f'/home/{user}/RH-ota/updater-config.json'):
    config_file_exists = True
else:
    config_file_exists = False


def internet_check(user):  # too much code - but works for now
    print("\nPlease wait - checking internet connection state...\n")
    before_millis = int(round(time.time() * 1000))
    os.system("rm index* > /dev/null 2>&1")
    os.system("timeout 10s wget www.github.com")
    while True:
        now_millis = int(round(time.time() * 1000))
        time_passed = (now_millis - before_millis)
        if os.path.exists("./index.html"):
            internet_flag = 1
            break
        elif time_passed > 10100:
            internet_flag = 0
            break
    os.system(f"rm /home/{user}/RH-ota/index.html > /dev/null 2>&1")
    os.system(f"rm /home/{user}/RH-ota/wget-log* > /dev/null 2>&1")
    os.system(f"rm /home/{user}/index.html > /dev/null 2>&1")
    os.system(f"rm /home/{user}/wget-log* > /dev/null 2>&1")

    return internet_flag


def old_version_name_check():
    old_version_name = 0
    os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.old_version")
    os.system("sed -i 's/updater_version = //' ~/.ota_markers/.old_version")
    os.system("sed -i 's/#.*/ /' ~/.ota_markers/.old_version")
    f = open(f"/home/{user}/.ota_markers/.old_version", "r")
    for line in f:
        old_version_name = line
    return old_version_name


def new_version_name_check():
    new_version_name = 0
    os.system("grep 'updater_version =' ~/RH-ota/update.py > ~/.ota_markers/.new_version")
    os.system("sed -i 's/updater_version = //' ~/.ota_markers/.new_version")
    os.system("sed -i 's/#.*/ /' ~/.ota_markers/.new_version")
    f = open(f"/home/{user}/.ota_markers/.new_version", "r")
    for line in f:
        new_version_name = line
    return new_version_name


def self_update():
    internet_flag = internet_check(user)
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Update canceled.\n")
        sleep(2)
    else:
        print("\nInternet connection - OK\n")
        sleep(1.5)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")  # resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")  # resolves compatibility issues
        old_version_name = old_version_name_check()
        print(f"\n\n\n\t Please wait: updating process from version {old_version_name}\n\n")
        dots_show(2)
        if config_file_exists:
            os.system("cp ~/RH-ota/updater-config.json ~/.ota_markers/updater-config.json")
        if beta_tester_update:
            print("Update won't contain PDF file - may be changed in config file.\n")
            os.system("sudo rm -rf ~/RH-ota*")
            os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
            os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip")
            os.system("unzip tempota.zip")
            os.system("rm tempota.zip")
            os.system("mv RH-ota-* RH-ota")
        if not beta_tester_update:
            if not no_pdf_update:
                print("Update will contain PDF file - may be changed in config file.\n")
                os.system("sudo rm -rf ~/RH-ota*")
                os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
                os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/main_stable -O tempota.zip")
                os.system("unzip tempota.zip")
                os.system("rm tempota.zip")
                os.system("mv RH-ota-* RH-ota")
            elif no_pdf_update:
                print("Update won't contain PDF file - may be changed in config file.\n")
                os.system("sudo rm -rf ~/RH-ota*")
                os.system("rm tempota.zip > /dev/null  > /dev/null 2>&1")
                os.system("wget https://codeload.github.com/szafranski/RH-ota/zip/no_pdf -O tempota.zip")
                os.system("unzip tempota.zip")
                os.system("rm tempota.zip")
                os.system("mv RH-ota-* RH-ota")
        if config_file_exists:
            os.system("cp ~/.ota_markers/updater-config.json ~/RH-ota/updater-config.json")
        new_version_name = new_version_name_check()
        print(f"\n\n\n\t RotorHazard OTA Manager updated to version {new_version_name}\
        \n\t\tYou may check update-notes.\n\n")
        sleep(1)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")  # resolves compatibility & permissions issues
        if new_version_name != old_version_name:
            os.system("echo OTA was updated > ~/.ota_markers/.was_updated")


def main():
    internet_check(user)
    self_update()


if __name__ == "__main__":
    main()
