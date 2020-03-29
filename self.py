from time import sleep
import os
import shutil
from modules import load_config, dots_show, internet_check, get_ota_version


def self_update(config):
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Update canceled.\n")
        sleep(2)
    else:
        print("\nInternet connection - OK\n")
        sleep(1.5)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")  # resolves compatibility issues
        os.system("sudo chmod -R 777 ~/RH-ota > /dev/null 2>&1")  # resolves compatibility issues
        old_version_name = get_ota_version()
        print(f"\n\n\n\t Please wait: updating process from version {old_version_name}\n\n")
        dots_show(2)
        source = 0
        if config:  # if config is not empty, then the file exited to load.
            shutil.copyfile('~/RH-ota/updater-config.json', '~/.ota_markers/updater-config.json')
        if config['beta_tester']:
            source = 'master'
            print("This will be 'beta' update - may be changed in config file.\n")
        if not config['beta_tester']:
            if not config.updates_without_pdf:
                source = 'main_stable'
                print("Update will contain PDF file - may be changed in config file.\n")
            else:
                source = 'no_pdf'
                print("Update won't contain PDF file - may be changed in config file.\n")
        os.system(f". ./scripts/self_updater_actions.sh {source}")
        if config:  # if the config variable is not empty, then the config file must have existed.
            shutil.copyfile('~/.ota_markers/updater-config.json', '~/RH-ota/updater-config.json"')
        new_version_name = get_ota_version()
        print(f"\n\n\n\t RotorHazard OTA Manager updated to version {new_version_name}\
        \n\t\tYou may check update-notes.\n\n")
        sleep(1)
        os.system("sudo chmod -R 777 ~/.ota_markers > /dev/null 2>&1")
        os.system("sudo chmod -R 777 ~/RH-ota/*.sh > /dev/null 2>&1")  # only make the shell scripts executable.
        if new_version_name != old_version_name:
            os.system("echo OTA was updated > ~/.ota_markers/.was_updated")
            # todo change to read json "was_updated"


def main():
    config = load_config()
    internet_check()
    self_update(config)


if __name__ == "__main__":
    main()
