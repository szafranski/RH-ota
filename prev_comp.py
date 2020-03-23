import os
from modules import check_if_string_in_file, load_config, copy_file
from configparser import ConfigParser
from pathlib import Path


def prev_comp(parser, home_dir):
    aliases_1_flag = False
    aliases_2_flag = False
    installation_flag = False
    updater_flag = False
    serial_flag = False
    pinout_flag = False

    # if os.stat(homedir+'/.ota_markers/ota_config.txt').st_size == 0:
    #    os.system("rm {homedir}/.ota_markers/ota_config.txt > /dev/null 2>&1")

    Path(f"{home_dir}/.ota_markers").mkdir(exist_ok=True)
    if os.path.exists(f"{home_dir}/.aliases_added"):
        copy_file(f"{home_dir}/.aliases_added", f"{home_dir}/.ota_markers/.aliases_added")

    if not os.path.exists(home_dir + "/.ota_markers/.aliases_added"):
        copy_file(f"{home_dir}/.updater_self", f"{home_dir}/.ota_markers/.updater_self")

    if not os.path.exists(home_dir + "/.ota_markers/.installation-check_file.txt"):
        copy_file(f"{home_dir}/.old_RotorHazard.old/.installation-check_file.txt",
                  f"{home_dir}/.ota_markers/.installation-check_file.txt")

    copy_file(f"{home_dir}/.serialok", f"{home_dir}/.ota_markers/.serialok")
    if os.path.exists(home_dir + "/.bashrc"):  # aliases compatibility
        if check_if_string_in_file(home_dir + '/.bashrc', 'RotorHazard OTA Manager updated'):
            os.system(f"sed -i 's/alias updateupdater/# alias updateupdater/g' {home_dir}/.bashrc")
            os.system(f"sed -i 's/RotorHazard OTA Manager updated/old alias/g' {home_dir}/.bashrc")
            os.system("echo 'alias updateupdater=\"cd ~ && sudo cp ~/RH-ota/self.py ~/.ota_markers/self.py \
            && sudo python ~/.ota_markers/self.py \"  # part of self-updater' | tee -a ~/.bashrc >/dev/null")
        if check_if_string_in_file(home_dir + '/.bashrc', 'starts the server'):
            os.system(f"sed -i 's/alias ss/# alias ss/g' {home_dir}/.bashrc")
            os.system(f"sed -i 's/starts the server/old alias/g' {home_dir}/.bashrc")
            os.system("echo 'alias ss=\"cd ~/RotorHazard/src/server && python server.py\"   #  starts the RH-server' \
            | tee -a ~/.bashrc >/dev/null")
        if check_if_string_in_file(home_dir + '/.bashrc', 'opens updating script'):
            os.system(f"sed -i 's/alias ota=/# alias ota=/g' {home_dir}/.bashrc")
            os.system(f"sed -i 's/opens updating script/old alias/g' {home_dir}/.bashrc")
            os.system("echo 'alias ota=\"cd ~/RH-ota && python update.py\"  # opens updating soft' \
            | tee -a ~/.bashrc >/dev/null")
        if check_if_string_in_file(home_dir + '/.bashrc', 'opens updating script'):
            os.system(f"sed -i 's/alias ota=/# alias ota=/g' {home_dir}/.bashrc")
            os.system(f"sed -i 's/opens updating script/old alias/g' {home_dir}/.bashrc")
            os.system("echo 'alias ota=\"cd ~/RH-ota && python3 update.py\"  # opens updating soft' \
            | tee -a ~/.bashrc >/dev/null")
        if check_if_string_in_file(home_dir + '/.bashrc', 'opens updating soft'):
            os.system(f"sed -i 's/alias ota=/# alias ota=/g' {home_dir}/.bashrc")
            os.system(f"sed -i 's/opens updating script/old alias/g' {home_dir}/.bashrc")
            os.system("echo 'alias ota=\"cd ~/RH-ota && python3 update.py\"  # opens ota soft' \
            | tee -a ~/.bashrc >/dev/null")

            #  todo change?
            #  todo stupid aliases update have to be fixed
            # is this file necesarry? abandon with python3 implementation or make it "smaller"

        if check_if_string_in_file(home_dir + '/.bashrc', 'part of self-updater'):
            os.system(f"sed -i 's/part of self-updater/part of self updater/g' {home_dir}/.bashrc")
            os.system("echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py \
            && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null")
            if not os.path.exists(home_dir + "/.ota_markers/.aliases2_added"):
                os.system("echo 'alias otacfg=\"nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' \
                | tee -a ~/.bashrc >/dev/null")
                os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && cp distr-updater-config.json updater-config.json \"  \
                # copies ota conf. file' | tee -a ~/.bashrc >/dev/null")
                os.system("echo 'alias home=\"cd ~ \"  # go homedir (without ~ sign)' | tee -a ~/.bashrc >/dev/null")
                os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases2_added \
                >/dev/null")
        if os.path.exists("./updater-config.json"):  # json compatibility
            if not check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"pins_assignment"'):
                os.system(f"sed -i 's/\"debug_mode\" : 0/\"debug_mode\" : 0,/g' {home_dir}/RH-ota/updater-config.json")
                os.system(f"sed -i 's/\"debug_mode\" : 1/\"debug_mode\" : 1,/g' {home_dir}/RH-ota/updater-config.json")
                os.system("sed -i 's/}/    \"pins_assignment\" : \"default\" /g' "
                          + home_dir + "/RH-ota/updater-config.json")
                os.system("echo '}' | tee -a " + home_dir + "/RH-ota/updater-config.json >/dev/null 2>&1")
            if check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"pins_assignment"'):
                if not check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"updates_without_pdf"'):
                    os.system(f"sed -i 's/\"pins_assignment\" : \"default\"/\"pins_assignment\" : \"default\",/g' \
    {home_dir}/RH-ota/updater-config.json")
                    os.system(f"sed -i 's/\"pins_assignment\" : \"custom\"/\"pins_assignment\" : \"custom\",/g' \
    {home_dir}/RH-ota/updater-config.json")
                    os.system(f"sed -i 's/\"pins_assignment\" : \"PCB\"/\"pins_assignment\" : \"PCB\",/g' \
    {home_dir}/RH-ota/updater-config.json")
                    os.system("sed -i 's/}/    \"updates_without_pdf\" : 0 /g' "
                              + home_dir + "/RH-ota/updater-config.json")
                    os.system("echo '}' | tee -a " + home_dir + "/RH-ota/updater-config.json >/dev/null 2>&1")
            if check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"updates_without_pdf"'):
                if not check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"pi_4_cfg"'):
                    os.system(f"sed -i 's/\"updates_without_pdf\" : 0/\"updates_without_pdf\" : 0,/g' \
    {home_dir}/RH-ota/updater-config.json")
                    os.system(f"sed -i 's/\"updates_without_pdf\" : 1/\"updates_without_pdf\" : 1,/g' \
    {home_dir}/RH-ota/updater-config.json")
                    os.system("sed -i 's/}/    \"pi_4_cfg\" : 0 /g' " + home_dir + "/RH-ota/updater-config.json")
                    os.system("echo '}' | tee -a " + home_dir + "/RH-ota/updater-config.json >/dev/null 2>&1")
            if check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"pi_4_cfg"'):
                if not check_if_string_in_file(home_dir + '/RH-ota/updater-config.json', '"beta_tester"'):
                    os.system(f"sed -i 's/\"pi_4_cfg\" : 0/\"pi_4_cfg\" : 0,/g' {home_dir}/RH-ota/updater-config.json")
                    os.system(f"sed -i 's/\"pi_4_cfg\" : 1/\"pi_4_cfg\" : 1,/g' {home_dir}/RH-ota/updater-config.json")
                    os.system("sed -i 's/}/    \"beta_tester\" : 0 /g' " + home_dir + "/RH-ota/updater-config.json")
                    os.system("echo '}' | tee -a " + home_dir + "/RH-ota/updater-config.json >/dev/null 2>&1")
    if os.path.exists(home_dir + "/.ota_markers/.serialok"):
        serial_flag = True
    if os.path.exists(home_dir + "/.ota_markers/.installation-check_file.txt"):
        installation_flag = True
    if os.path.exists(home_dir + "/.ota_markers/.pinout_added"):
        pinout_flag = True
    if os.path.exists(home_dir + "/.ota_markers/.aliases_added"):
        aliases_1_flag = True
    if os.path.exists(home_dir + "/.ota_markers/.aliases2_added"):
        aliases_2_flag = True
    if os.path.exists(home_dir + "/.ota_markers/.updater_self"):
        updater_flag = True
    if not os.path.exists(home_dir + "/.ota_markers/ota_config.txt"):
        copy_file(f"{home_dir}/RH-ota/resources/ota_config.txt", f"{home_dir}/.ota_markers/ota_config.txt")
    parser.read(home_dir + '/.ota_markers/ota_config.txt')
    if aliases_1_flag:
        parser.set('added_functions', 'aliases_1', '1')
    if aliases_2_flag:
        parser.set('added_functions', 'aliases_2', '1')
    if installation_flag:
        parser.set('added_functions', 'installation_done', '1')
    if updater_flag:
        parser.set('added_functions', 'updater_planted', '1')
    if pinout_flag:
        parser.set('added_functions', 'pinout_installed', '1')
    if serial_flag:
        parser.set('added_functions', 'serial_added', '1')
    with open(home_dir + '/.ota_markers/ota_config.txt', 'w') as configfile:
        parser.write(configfile)
    if not check_if_string_in_file(home_dir + '/.ota_markers/ota_config.txt', 'curl_installed'):
        os.system(f"echo curl_installed = 0 | tee -a {home_dir}/.ota_markers/ota_config.txt > /dev/null ")
    if not check_if_string_in_file(home_dir + '/.ota_markers/ota_config.txt', 'configparser_installed'):
        os.system(f"echo configparser_installed = 0 | tee -a {home_dir}/.ota_markers/ota_config.txt > /dev/null ")
    if not check_if_string_in_file(home_dir + '/.ota_markers/ota_config.txt', 'python3_installed'):
        os.system(f"echo python3_installed = 0 | tee -a {home_dir}/.ota_markers/ota_config.txt > /dev/null")


'''
We create a main method to capture the context for any variables
we want to build in this script when running standalone. 

main() is only called if you run this script from the command line directly eg:
python3 prev_comp.py

it will NOT be called if you import this file into another file.
'''


def main():
    parser, config = load_config()
    home_dir = os.path.expanduser('~')
    prev_comp(parser, home_dir)


'''
This if statement is responsible for detecting if this script 
was run from command line.  it is only true when this script
is run from the console. 
'''
if __name__ == "__main__":
    main()
