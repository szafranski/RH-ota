from time import sleep
import os
import sys
import json
from modules import clear_the_screen, bcolors, logo_top

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

    print("""Step 4.""")

    print("""
Connect PC to WiFi network:
name: RH-TIMER
password: timerpass
if you have any problems connecting wifi with new name - try "forgetting" the (old) network in PC's WiFi settings and than try again

Now you should be able to enter the network typing in the browser:
10.10.10.10:5000 - using WiFi
172.20.20.20:5000 - using ethernet.""")

    print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
            +bcolors.YELLOW+"""    Exit by pressing 'e'"""+bcolors.ENDC+"""\n""")
    selection=str(raw_input(""))
    if selection=='r':
        os.system("sudo reboot")
    if selection=='e':
        sys.exit()
    else :
        main()

def step_three():

    print("""\n\t\tStep 3.\n""")
    os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.ap")
    print("""\n\tAfter rebooting you can connect to the timer, via Wifi or ethernet.\n 
    WiFi: 10.10.10.10:5000 (10.10.10.10:5000 if connecting from a browser)
    ethernet: 172.20.20.20 (172.20.20.20:5000 if connecting from a browser)\n\n
    You can enter Access Point extra menu after rebooing
    and check how you can connect to the internet.\n""")
    print("""\n\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t"""
            +bcolors.YELLOW+"""    Exit by pressing 'e'"""+bcolors.ENDC+"""\n""")
    selection=str(raw_input(""))
    if selection=='r':
        os.system("sudo reboot")
    if selection=='e':
        sys.exit()
    else :
        main()

def step_two():
    print("""\n\n
    Step 2.\n
Next step requires performing some actions in GUI.
You may write those informations down or take a picture etc.
You can also print file 'step_two.txt' from 'net_ap' folder.
Remember to do it BEFORE rebooting.
After performing step 2. and connecting to timer again, 
come back to this menu and enter step 3.
    
connect PC to WiFi network: 
name: raspi-webgui
password: ChangeMe

enter IP address: 10.3.141.1 in browser
Username: admin
Password: secret  

Click:
Configure hotspot -> SSID (enter name you want, eg. "RH-TIMER") 

Wireless Mode (change to 802.11n - 2.4GHz)

save settings 

Click:
Configure hotspot -> security tab

PSK (enter password that you want to have, eg. "timerpass")

save settings

DON'T CHANGE OTHER SETTINGS IN GUI!  


Read carefully whole instruction from above before rebooting!""")

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
    os.system("echo 'country="+myPlace+"'| sudo  tee -a /boot/config.txt")
    os.system("sudo apt-get update && sudo apt-get upgrade -y")
    os.system("sudo apt install curl -y")
    os.system("curl -sL https://install.raspap.com | bash -s -- -y")
    step_two()
    print("""\n\t\t\t"""+bcolors.GREEN+"""Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t"""
            +bcolors.YELLOW+"""Exit by pressing 'e'"""+bcolors.ENDC+"""\n""")
    selection=str(raw_input(""))
    if selection=='r':
        os.system("sudo reboot")
    if selection=='e':
        sys.exit()
    else :
        main()

def step_zero():
    clear_the_screen()
    sleep(0.05)
    print("""\n\n
    After performing this process your Raspberry Pi can be used as standalone\n
    Access Point. You won't need additional router for connecting with it. \n
    You will loose ability of connecting Raspberry wirelessly to any router or hotspot.\n
    You will still have ability to connect it to the Internet sharing device, \n
    like router or PC via ethernet cable. You will also be able to connect with the timer\n
    via Wifi from PC or mobile phone etc. - if you had range. \n
    If during this process you would want to check detailed instructions,\n
    you can enter 'net_ap' folder from this repo, on your mobile phone etc.\n
    This process will require few reboots. Do you want to continue?\n""")
    print("""\n
    \t"""+bcolors.GREEN+"""'y' - Yes, let's do it """+bcolors.ENDC+"""\n
    \t'3' - enters "Step 3." - check it after first two steps\n
    \t'x' - enters Access Point extra menu - check it after operation\n
    \t"""+bcolors.YELLOW+"""'e' - exit to main menu"""+bcolors.ENDC+"""\n""")
    selection=str(raw_input(""))
    if selection=='y':
        step_one()
    if selection=='3':
        step_three()
    if selection=='x':
        ap_menu()
    if selection=='e':
        sys.exit()
    else :
        main()

def ap_menu():
    def second_page():
        clear_the_screen()
        print("""\n
    When Raspberry configuration has been changed so it performs
    as Access Point or as a DHCP client (normal mode),
    configuration file is being copied with a proper name.
    Next you have to reboot, so changes can be applied.
    When you setup Pi as a client, you can just connect
    it to the router. If you are using PC as a internet sharing
    device, you have to enable that option in OS settings.
    Instructions for Windows can be found in net_ap folder.\n
    
    If you want to connect to Raspberry via SSH or VNC,
    when it's in client mode you have to know its IP address.
    Check it in router settings page or using special program 
    'Advanced IP Scanner' on a PC. If you are using Pi as a AP, 
    its IP is always 172.20.20.20 (ethernet). Remember to disable
    internet sharing functionality on your PC's OS, when Raspberry
    is in Access Point mode. \n
    Remember that you can always connect to the timer (eg. from yet 
    another device) via WiFi. It's wireless IP is 10.10.10.10.\n
    You can also read/print those instructions. File 'detailed.txt',
    in net_ap folder.
    \n""")
        selection=str(raw_input("\t\t"+bcolors.GREEN+"'k' - OK '"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
        if selection=='k':
            sys.exit()
        if selection=='b':
            first_page()
        else :
            second_page()
    def first_page():
        clear_the_screen()
        logo_top()
        sleep(0.05)
        print("""\n
    Right now you have your Access Point configured. However,
    there is still an option to mantain internet connection.
    You will be able to connect the Pi via ethernet to the router 
    or PC - with internet sharing option enbled. It requires chages
    in configuration file. Those will be performed automatically,
    after entering 'netcfg' or 'apcfg' in command line.
    Remember to reboot the timer after every change. Instruction
    can be also found in 'apconf.txt' file in net_ap folder.\n
    Remember that regardless how you have your Raspberry configured
    in a given moment, you can always connect to it using WiFi.
    It can be helpful if you don't remember how your timer was configured
    when you left it or when some troubleshooting is required.\n
    Open second page, for detailed explanation.\n\n""")
        selection=str(raw_input("\t\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
        if selection=='s':
            secondPage()
        if selection=='b':
            main()
        else :
            first_page()
    first_page()

def main():
    step_zero()
    step_one()
main()
