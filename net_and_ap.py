import os
import sys
from modules import clear_the_screen, Bcolors, logo_top, load_config


# Set the WiFi country in raspi-config's Localisation Options:
# sudo raspi-config
# ( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )


def step_four():
    print("""Step 4.

    
Connect PC to WiFi network:
name: RH-TIMER
password: timerpass
if you have any problems connecting wifi with new name - try "forgetting" the (old) network in PC's WiFi settings 
and than try again

Now you should be able to enter the network typing in the browser:
10.10.10.10:5000 - using WiFi
172.20.20.20:5000 - using ethernet.""")

    print(f"""{Bcolors.GREEN}
            Reboot by pressing 'r' {Bcolors.ENDC}{Bcolors.YELLOW} 
            Exit by pressing 'e'{Bcolors.ENDC}
            """)
    selection = input()
    if selection == 'r':
        os.system("sudo reboot")
    if selection == 'e':
        sys.exit()
    else:
        main()


def step_three():
    print("\n\t\tStep 3.\n")
    os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.ap")
    print("""
    After rebooting you can connect to the timer, via Wifi or ethernet. 
    WiFi: 10.10.10.10:5000 (10.10.10.10:5000 if connecting from a browser)
    ethernet: 172.20.20.20 (172.20.20.20:5000 if connecting from a browser)
    
    You can enter Access Point extra menu after rebooting
    and check how you can connect to the internet.
    """)
    print(f"""{Bcolors.GREEN} 
                Reboot by pressing 'r' {Bcolors.ENDC}{Bcolors.YELLOW}
                Exit by pressing 'e'{Bcolors.ENDC}
            """)
    selection = input()
    if selection == 'r': os.system("sudo reboot")
    if selection == 'e': sys.exit()
    else: main()


def step_two():
    print("""Step 2.
        
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


def step_one(config):
    conf_copy()
    os.system("sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf")
    os.system(f"echo 'country={config.country}'| sudo  tee -a /boot/config.txt")
    os.system("sudo apt-get update && sudo apt-get upgrade -y")
    os.system("sudo apt install curl -y")
    os.system("curl -sL https://install.raspap.com | bash -s -- -y")
    step_two()
    print(f"""{Bcolors.GREEN}
                Reboot by pressing 'r' {Bcolors.ENDC}{Bcolors.YELLOW}
                Exit by pressing 'e'{Bcolors.ENDC}
            """)
    selection = input()
    if selection == 'r':
        os.system("sudo reboot")
    if selection == 'e': sys.exit()
    else: main()


def step_zero(config):
    clear_the_screen()
    print("""
    After performing this process your Raspberry Pi can be used as standalone
    Access Point. You won't need additional router for connecting with it. 
    You will loose ability of connecting Raspberry wirelessly to any router or hotspot.
    You will still have ability to connect it to the Internet sharing device, 
    like router or PC via ethernet cable. You will also be able to connect with the timer
    via Wifi from PC or mobile phone etc. - if you had range. 
    If during this process you would want to check detailed instructions,
    you can enter 'net_ap' folder from this repo, on your mobile phone etc.
    This process will require few reboots. Do you want to continue?
    """)
    print(f"""{Bcolors.GREEN}
            'y' - Yes, let's do it{Bcolors.ENDC}
            '3' - enters "Step 3." - check it after first two steps
            'x' - enters Access Point extra menu - check it after operation{Bcolors.YELLOW}
            'e' - exit to main menu{Bcolors.ENDC}
            """)
    selection = input()
    if selection == 'y': step_one(config)
    if selection == '3': step_three()
    if selection == 'x': ap_menu(config)
    if selection == 'e': sys.exit()
    else: main()


def ap_menu(config):
    def second_page():
        clear_the_screen()
        print("""
    When Raspberry configuration has been changed so it performs
    as Access Point or as a DHCP client (normal mode),
    configuration file is being copied with a proper name.
    Next you have to reboot, so changes can be applied.
    When you setup Pi as a client, you can just connect
    it to the router. If you are using PC as a internet sharing
    device, you have to enable that option in OS settings.
    Instructions for Windows can be found in net_ap folder.
    
    If you want to connect to Raspberry via SSH or VNC,
    when it's in client mode you have to know its IP address.
    Check it in router settings page or using special program 
    'Advanced IP Scanner' on a PC. If you are using Pi as a AP, 
    its IP is always 172.20.20.20 (ethernet). Remember to disable
    internet sharing functionality on your PC's OS, when Raspberry
    is in Access Point mode. 
    
    Remember that you can always connect to the timer (eg. from yet 
    another device) via WiFi. It's wireless IP is 10.10.10.10.
    
    You can also read/print those instructions. File 'detailed.txt',
    in net_ap folder.
    """)
        selection = input(f"""{Bcolors.GREEN}
                'k' - OK '{Bcolors.ENDC}{Bcolors.YELLOW}
                'b' - go back{Bcolors.ENDC}""")
        if selection == 'k': sys.exit()
        if selection == 'b': first_page(config)
        else: second_page()

    def first_page(config):
        clear_the_screen()
        logo_top(config.debug_mode)
        print("""\n
    Right now you have your Access Point configured. However,
    there is still an option to maintain internet connection.
    You will be able to connect the Pi via ethernet to the router 
    or PC - with internet sharing option enbled. It requires chages
    in configuration file. Those will be performed automatically,
    after entering 'netcfg' or 'apcfg' in command line.
    Remember to reboot the timer after every change. Instruction
    can be also found in 'apconf.txt' file in net_ap folder.
    
    Remember that regardless how you have your Raspberry configured
    in a given moment, you can always connect to it using WiFi.
    It can be helpful if you don't remember how your timer was configured
    when you left it or when some troubleshooting is required.
    
    Open second page, for detailed explanation.
    """)
        selection = input(f"""{Bcolors.GREEN}
                's' - second page'{Bcolors.ENDC}{Bcolors.YELLOW}
                'b' - go back
                """)
        if selection == 's': second_page()
        if selection == 'b': main()
        else: first_page(config)

    first_page(config)


def net_and_ap_conf(config):
    step_zero(config)
    step_one(config)


def main():
    config = load_config()
    net_and_ap_conf(config)


if __name__ == "__main__":
    main()
