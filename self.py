from time import sleep
import os
import shutil
from modules import load_config, dots_show, internet_check, get_ota_version


def make_directories_accessible(config):
    markers_dir = f'/home/{config.user}/.ota_markers'
    ota_dir = f'/home/{config.user}/RH-ota'
    os.system(f"sudo chmod -R 777 {markers_dir} > /dev/null 2>&1") if os.stat(markers_dir).st_uid == 0 else None
    os.system(f"sudo chmod -R 777 {ota_dir} > /dev/null 2>&1") if os.stat(ota_dir).st_uid == 0 else None


def self_update(config):
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Update canceled.\n")
        sleep(2)
    else:
        print("\nInternet connection - OK\n")
        sleep(1.5)
        make_directories_accessible(config)
        old_version_name = get_ota_version()
        print(f"\n\n\n\t Please wait: updating process from version {old_version_name}\n\n")
        dots_show(2)
        # if config:  # if config is not empty, then the file exited to load.
        #     shutil.copyfile('~/RH-ota/updater-config.json', '~/.ota_markers/updater-config.json')
        if config.beta_tester:
            source = 'master'
            print("This will be the 'beta' update - may be changed in config file.\n")
        else:
            source = 'main_stable'
        os.system(f"./scripts/self_updater.sh {source}")
        if config:  # if the config variable is not empty, then the config file must have existed.
            shutil.copyfile("~/.ota_markers/old_RH-ota/updater-config.json", "~/RH-ota/updater-config.json")
        new_version_name = get_ota_version()
        print(f"""
    
    RotorHazard OTA Manager updated to version {new_version_name}
    
            You may check update-notes.

            """)
        sleep(1)
        make_directories_accessible(config)
        if new_version_name != old_version_name:
            os.system("echo OTA was updated > ~/.ota_markers/.was_updated")


def main():
    config = load_config()
    internet_check()
    self_update(config)


if __name__ == "__main__":
    main()
