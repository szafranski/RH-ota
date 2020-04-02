from time import sleep
import os
import sys
import json
from modules import Bcolors, clear_the_screen, logo_top

if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']

myPlace = data['country']


# Set the WiFi country in raspi-config's Localisation Options:
# sudo raspi-config
# ( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )

def step_four():
    with open('./net_ap/net_steps.txt', 'rt') as f:
        for line in f:
            if '### step4' in line:
                for line in f:
                    line.replace('####', '')
                    if '####' in line:
                        break
    print("""\n\t\t\t\t""" + Bcolors.GREEN + """    Reboot by pressing 'r' """ + Bcolors.ENDC + """\n\n\t\t\t\t"""
          + Bcolors.YELLOW + """    Exit by pressing 'e'""" + Bcolors.ENDC)
    selection = str(input(""))
    if selection == 'r':
        os.system("sudo reboot")
    if selection == 'e':
        sys.exit()
    else:
        main()


def step_three():
    os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.ap")
    clear_the_screen()
    with open('./net_ap/net_steps.txt', 'rt') as f:
        for line in f:
            if '### step3' in line:
                for line in f:
                    line.replace('####', '')
                    if '####' in line:
                        break
    print("""\n\t\t\t\t""" + Bcolors.GREEN + """    Reboot by pressing 'r' """ + Bcolors.ENDC + """\n\n\t\t\t\t"""
          + Bcolors.YELLOW + """    Exit by pressing 'e'""" + Bcolors.ENDC + """\n""")
    selection = str(input(""))
    if selection == 'r':
        os.system("sudo reboot")
    if selection == 'e':
        sys.exit()
    else:
        main()


def step_two():
    clear_the_screen()
    with open('./net_ap/net_steps.txt', 'rt') as f:
        for line in f:
            if '### step2' in line:
                for line in f:
                    line.replace('\n', '').replace('####', '')
                    if '####' in line:
                        break


def conf_copy():
    os.system("echo 'alias netcfg=\"cp /etc/dhcpcd.conf.net /etc/dhcpcd.conf \"  # net conf' | sudo tee -a ~/.bashrc")
    os.system("echo 'alias apcfg=\"cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf \"  # net conf' | sudo tee -a ~/.bashrc")
    os.system("sudo cp ./net_ap/dhcpcd.conf.net /etc/dhcpcd.conf.net")
    os.system("sudo cp ./net_ap/dhcpcd.conf.ap /etc/dhcpcd.conf.ap")
    os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig")
    os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig")
    os.system("sudo cp ./net_ap/dnsmasq.conf.net /etc/dnsmasq.conf.net")


def step_one():
    conf_copy()
    os.system("sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system("echo 'country=" + myPlace + "'| sudo  tee -a /boot/config.txt")
    os.system("sudo apt-get update && sudo apt-get upgrade -y")
    os.system("sudo apt install curl -y")
    os.system("curl -sL https://install.raspap.com | bash -s -- -y")
    step_two()
    print("""\n\t\t\t\t""" + Bcolors.GREEN + """Reboot by pressing 'r' """ + Bcolors.ENDC + """\n\n\t\t\t\t"""
          + Bcolors.YELLOW + """Exit by pressing 'e'""" + Bcolors.ENDC + """\n""")
    selection = str(input(""))
    if selection == 'r':
        os.system("sudo reboot")
    if selection == 'e':
        sys.exit()
    else:
        main()


def step_zero():
    sleep(0.05)
    clear_the_screen()
    sleep(0.05)
    logo_top()
    sleep(0.05)
    with open('./net_ap/net_steps.txt', 'rt') as f:
        for line in f:
            if '### step1' in line:
                for line in f:
                    line.replace('\n', '').replace('####', '')
                    if '####' in line:
                        break
    print("""\n
    \t\t""" + Bcolors.GREEN + """'y' - Yes, let's do it """ + Bcolors.ENDC + """\n
    \t\t'3' - enters "Step 3." - check it after first two steps\n
    \t\t'x' - enters Access Point extra menu - info after operation\n
    \t\t""" + Bcolors.YELLOW + """'e' - exit to main menu""" + Bcolors.ENDC + """\n""")
    selection = str(input(""))
    if selection == 'y':
        step_one()
    if selection == '3':
        step_three()
    if selection == 'x':
        ap_menu()
    if selection == 'e':
        sys.exit()
    else:
        main()


def ap_menu():
    def second_page():
        sleep(0.05)
        clear_the_screen()
        sleep(0.05)
        with open('./net_ap/net_steps.txt', 'rt') as f:
            for line in f:
                if '### step last - page 2' in line:
                    for line in f:
                        line.replace('\n', '').replace('####', '')
                        if '####' in line:
                            break
        selection = input("\t\t\t" + Bcolors.GREEN + "'k' - OK '" + Bcolors.ENDC
                          + "\t\t" + Bcolors.YELLOW + "'b' - go back" + Bcolors.ENDC + "\n")
        if selection == 'k':
            sys.exit()
        if selection == 'b':
            first_page()
        else:
            second_page()

    def first_page():
        sleep(0.05)
        clear_the_screen()
        sleep(0.05)
        logo_top()
        sleep(0.05)
        with open('./net_ap/net_steps.txt', 'rt') as f:
            for line in f:
                if '### step last - page 1' in line:
                    for line in f:
                        line.replace('\n', '').replace('####', '')
                        if '####' in line:
                            break
        selection = input("\t\t\t" + Bcolors.GREEN + "'s' - second page'" + Bcolors.ENDC + "\t\t"
                          + Bcolors.YELLOW + "'b' - go back" + Bcolors.ENDC + "\n")
        if selection == 's':
            second_page()
        if selection == 'b':
            main()
        else:
            first_page()

    first_page()


def main():
    step_zero()
    step_one()


if __name__ == "__main__":
    main()
