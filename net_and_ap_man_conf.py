import os
from modules import clear_the_screen, Bcolors, load_config


# Set the WiFi country in raspi-config's Localisation Options:
# sudo raspi-config
# ( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )


def step_four():
    while True:
        print("""Step 4.

    
    Connect PC to WiFi network:
    name: RH-TIMER
    password: timerpass
    if you have any problems connecting wifi with new name, 
    try "forgetting" the (old) network in PC's WiFi settings 
    and than try again
    
    Now you should be able to enter the timer typing in the browser:
    10.10.10.10 (or: 10.10.10.10:5000) - using WiFi
    172.20.20.20 (or: 172.20.20.20:5000) - using ethernet.


            {green}Reboot by pressing 'r'{endc} 
            
           {yellow}Exit by pressing 'e'{endc}
            """.format(yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S, endc=Bcolors.ENDC))
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        elif selection == 'e':
            break
        else:
            main()


def step_three():
    while True:
        os.system("sudo cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf")
        os.system("sudo cp /etc/dnsmasq.conf.ap /etc/dnsmasq.conf")
        print("""
        
                {bold}Step 3.{endc}
                
    After rebooting you can connect to the timer, via Wifi or ethernet. 
    WiFi: 10.10.10.10 (or: 10.10.10.10:5000)
    ethernet: 172.20.20.20 (172.20.20.20:5000)
    
    You can enter Access Point extra menu after rebooting
    and check how you can connect to the internet.
    
    
                {green}r - Reboot by pressing{endc}
                
               {yellow}e - Exit by pressing{endc}
                """.format(bold=Bcolors.BOLD, yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S, endc=Bcolors.ENDC))
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        elif selection == 'e':
            break
        else:
            main()


def step_zero(config):

    def step_one(config):

        while True:
            after_installing_raspap = """
            
            {bold}Step 2.{endc}
    
    Next step requires performing some actions in GUI.
    You may write those information down or take a picture etc.
    You can also print file 'step_two.txt' from 'net_ap' folder.
    Remember to do it BEFORE rebooting.
    After performing step 2. and connecting to timer again, 
    come back to this menu and enter step 3.
    
    connect PC to WiFi network: 
    name: raspi-webgui
    password: ChangeMe
    
    enter IP address: 10.3.141.1 (or: 10.3.141.1:8080) in the browser
    Username: admin
    Password: secret  
    
    Click:
    "Hotspot" (left menu) -> SSID (enter name you want, eg. "RH-TIMER")
    
    Wireless Mode (change to 802.11n - 2.4GHz)
    
    save settings
    
    Click:
    "Security" tab
    
    PSK (enter password that you want to have, eg. "timerpass")
    
    save settings
    
    DON'T CHANGE ANY OTHER SETTINGS IN GUI!
    
    Click:
    "System" (left menu) and "Reboot"
    
    reboot and connect to newly-created WiFi network using new password 
    
    
    {red} -- Read carefully whole instruction from above before rebooting --{endc}
            
                    {green}r - Reboot by pressing{endc}

                   {yellow}e - Exit by pressing{endc}
            """.format(bold=Bcolors.BOLD, red=Bcolors.RED, endc=Bcolors.ENDC,
                       yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S)

            os.system(f"./scripts/hotspot_manual.sh {config.user}")
            os.system("curl -sL https://install.raspap.com | bash -s -- -y")
            print(after_installing_raspap)
            selection = input()
            if selection == 'r':
                os.system("sudo reboot")
            elif selection == 'e':
                break

    while True:
        clear_the_screen()
        print("""
        
    After performing this process your Raspberry Pi can be used as standalone
    Access Point. You won't need additional router for connecting with it. 
    You won't be able to connect to any router or hotspot wirelessly.
    You will still have ability to connect it to the Internet sharing device, 
    like router or PC via ethernet cable. You will also be able to connect with 
    the timer via Wifi from PC or mobile phone etc. - if you had range. 
    If during this process you would want to check detailed instructions,
    you can enter 'net_ap' folder from this repo, on your mobile phone etc.
    This process will require few reboots. Do you want to continue?
        
        
         {green}y - Yes, let's do it{endc}
    
                3 - Enter "Step 3." - check it after first two steps
    
                x - Enter Access Point extra menu - check it after operation
    
        {yellow}e - Exit to main menu{endc}
                """.format(yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S, endc=Bcolors.ENDC))
        selection = input()
        if selection == 'y':
            step_one(config)
        elif selection == '3':
            step_three()
        elif selection == 'x':
            ap_menu()
        elif selection == 'e':
            break
        else:
            main()


def ap_menu():
    def second_page():
        while True:
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

                {green}k - OK{endc}
                
               """.format(yellow=Bcolors.YELLOW_S, green=Bcolors.GREEN_S, endc=Bcolors.ENDC))
            selection = input()
            if selection == 'k':
                break

    def first_page():
        while True:
            clear_the_screen()
            print("""\n
    Right now you have your Access Point configured. However,
    there is still an option to maintain internet connection.
    You will be able to connect the Pi via ethernet to the router 
    or PC - with internet sharing option enabled. It requires changes
    in configuration file. Those will be performed automatically,
    after entering '{green}netcfg{endc}' or '{green}apcfg{endc}' in command line.
    Remember to reboot the timer after every change. Instruction
    can be also found in 'apconf.txt' file in net_ap folder.
    
    Remember that regardless how you have your Raspberry configured
    in a given moment, you can always connect to it using WiFi.
    It can be helpful if you don't remember how your timer was configured
    when you left it or when some troubleshooting is required.
    
    Open second page, for detailed explanation.
    
    
                {green_s}s - Second page{endc}
               
               {yellow}e - Exit to menu{endc}
                    """.format(yellow=Bcolors.YELLOW_S, green_s=Bcolors.GREEN_S, green=Bcolors.GREEN, endc=Bcolors.ENDC))
            selection = input()
            if selection == 's':
                second_page()
            elif selection == 'e':
                break

    first_page()


def net_and_ap_conf(config):
    step_zero(config)


def main():
    config = load_config()
    net_and_ap_conf(config)


if __name__ == "__main__":
    main()
