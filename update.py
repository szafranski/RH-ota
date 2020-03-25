import os
import sys
from time import sleep
from modules import clear_the_screen, Bcolors, logo_top, image_show, ota_image, load_config, parser_write


def compatibility(parser, home_dir):  # adds compatibility and fixes with previous versions
    pass  # todo made it work but this prev_comp needs redesign
    # from prev_comp import prev_comp
    # import prev_comp
    # prev_comp(parser, home_dir)


def config_check():
    if not os.path.exists("./updater-config.json"):
        print(f"""{Bcolors.BOLD}
        Looks that you haven't set up config file yet.
        Please read about configuration process - point 5
        and next enter configuration wizard - point 6.{Bcolors.ENDC}""")


def log_to_dev(parser, config):
    log_write(config)
    log_send(parser, config)


def log_write(config):
    os.chdir(f"/home/{config.user}/RH-ota")
    os.system("mkdir log_data > /dev/null 2>&1")
    os.system("rm log_data/log.txt > /dev/null 2>&1")
    os.system("echo >./ log_data / log.txt")
    os.system("echo FILE /boot/config.txt | tee -a  ./log_data/log.txt")
    os.system("echo -------------------------------------------- | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("cat /boot/config.txt | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("echo FILE /boot/cmdline.txt | tee -a  ./log_data/log.txt")
    os.system("echo -------------------------------------------- | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("cat /boot/cmdline.txt | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("echo FILE updater-config.json | tee -a  ./log_data/log.txt")
    os.system("echo -------------------------------------------- | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("cat ~/RH-ota/updater-config.json | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("echo FILE ~/.ota_markers/ota_config.txt | tee -a  ./log_data/log.txt")
    os.system("echo -------------------------------------------- | tee -a  ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    os.system("cat ~/.ota_markers/ota_config.txt | tee -a ./log_data/log.txt")
    os.system("echo | tee -a  ./log_data/log.txt")
    print("LOGGING TO FILE - DONE")
    sleep(1.5)


def log_send(parser, config):
    while True:
        selection = input("\n\n\tDo you want to send a log file for a review to the developer? [y/n] ")
        if selection == 'y' or selection == 'yes':
            if not parser.getint('added_functions', 'curl_installed'):
                if not os.system("sudo apt install curl cowsay"):
                    parser.set('added_functions', 'curl_installed', '1')
                    parser_write(parser, config)
            log_name = input("\n\tPlease enter your name so we know who sent a log file: ")
            print("\n\tPlease wait, file is being uploaded...\n")
            os.system("rm ./log_data/log_name.txt > /dev/null 2>&1")
            os.system("rm ./log_data/log_code.txt > /dev/null 2>&1")
            os.system(f"echo {log_name} > ./log_data/log_name.txt")
            os.system(f"curl --upload-file ./log_data/log.txt https://transfer.sh/{log_name}_log.txt \
                 | tee -a ./log_data/log_code.txt")
            print("\n")
            os.system("sed -i 's/https:\/\/transfer.sh\///g' ./log_data/log_code.txt")
            os.system(f"sed -i 's/\/{log_name}_log.txt//g' ./log_data/log_code.txt")
            print("\n___________________________\n")
            print("\nTell your favourite developer those:\n")
            print(f"User name: {log_name}")
            f = open("./log_data/log_code.txt", "r")
            code = ''
            for line in f:
                code = line
            print(f"\nUser code: {code}")
            print("\n___________________________\n")
            input("\n\nHit 'Enter' to continue\n\n")
            if not os.system("cowsay You are awesome! Fly safe."):
                sleep(3)
            break
        if selection == 'n' or selection == 'no':
            print("\n\n\tOK - you log file is stored under 'log.txt' name in RH-ota directory.")
            input("\n\n\tHit 'Enter' to continue\n\n")
            break


def updated_check(config):
    user = config.user
    if os.path.exists(f"/home/{user}/.ota_markers/.was_updated"):
        clear_the_screen()
        logo_top(config.debug_mode)
        print(""" {bold}
        Software was updated recently to the new version.

        You can read update notes now or check them later.


         {endc}  {green} 
        'r' - read update notes {endc}

        's' - skip and don't show again
            """.format(bold=Bcolors.BOLD_S, endc=Bcolors.ENDC, green=Bcolors.GREEN))
        selection = input()
        if selection == 'r':
            os.system("less ./docs/update-notes.txt")
        if selection == 's':
            pass
        else:
            updated_check(config)
        os.system(f"rm /home/{user}/.ota_markers/.was_updated >/dev/null 2>&1")


def first(parser, config, updater_version):
    parser.read(f'/home/{config.user}/.ota_markers/ota_config.txt')
    clear_the_screen()
    print("\n\n")
    image_show()
    print(f"\t\t\t{Bcolors.BOLD} Updater version: {str(updater_version)}{Bcolors.ENDC}")
    sleep(1)
    updated_check(config)


def avr_dude(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        avrdude_menu = """
                {red}{bold}
                            AVRDUDE MENU
                            
                {blue}    
                        'i' - Install avrdude {endc}{yellow}
                {bold}
                        'e' - Go back {endc}
                """.format(bold=Bcolors.BOLD, endc=Bcolors.ENDC,
                           blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S)
        print(avrdude_menu)
        selection = input()
        if selection == 'i':
            os.system("sudo apt-get update")
            os.system("sudo apt-get install avrdude -y")
            print("\nDone\n")
            sleep(2)
        if selection == 'e':
            break


def serial_menu(parser, config):
    def serial_content():
        os.system("echo 'enable_uart=1'| sudo tee -a /boot/config.txt")
        os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
        parser.set('added_functions', 'serial_added', '1')
        parser_write(parser, config)
        print("""
        
        Serial port enabled successfully
        You have to reboot Raspberry now. Ok?
        
        r - Reboot now{yellow}
        b - Go back{endc}
            """.format(endc=Bcolors.ENDC, yellow=Bcolors.YELLOW_S))
        selection_2 = input()
        if selection_2 == 'r':
            os.system("sudo reboot")
        if selection_2 == 'b':
            return

    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        menu = """
            Serial port has to be enabled. 
            Without it Arduinos cannot be programmed.
            Do you want to enable it now?
            
            {yellow}
            y - for yes 
            a - for abort{endc}
            """.format(endc=Bcolors.ENDC, yellow=Bcolors.YELLOW)
        selection = input(menu)
        if selection == 'y':
            if parser.getint('added_functions', 'serial_added'):
                print("\n\n\t\tLooks like you already enabled Serial port. \n\t\tDo you want to continue anyway?\n")
                selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
                if selection == 'y':
                    serial_content()
                    break
                if selection == 'a':
                    break
            else:
                serial_content()
                break
        if selection == 'a':
            break


def aliases_menu(parser, config):
    clear_the_screen()

    def aliases_content():
        os.system("cat ./resources/aliases.txt | tee -a ~/.bashrc")
        parser.set('added_functions', 'aliases_1', '1')
        parser.set('added_functions', 'aliases_2', '1')
        parser_write(parser, config)
        print("\n\n\t\t    Aliases added successfully")
        sleep(3)
        features_menu(parser, config)

    aliases = """
    Aliases in Linux act like shortcuts or references to another commands. 
    You can use them every time when you operates in the terminal window. 
    For example instead of typing 'python ~/RotorHazard/src/server/server.py' 
    you can just type 'ss' (server start) etc. Aliases can be modified and added 
    anytime you want. You just have to open '~./bashrc' file in text editor 
    - like 'nano'. After that you have reboot or type 'source ~/.bashrc'. 
    
    {bold}
        Alias            What it does    
        
        ss        -->    starts the RotorHazard server
        cfg       -->    opens RH config.json file
        rh        -->    goes to server file directory
        py        -->    instead of 'python' - pure laziness
        sts       -->    stops RH service if was started
        otadir    -->    goes to RH server file directory
        ota       -->    opens this software
        als       -->    opens the file that contains aliases
        rld       -->    reloads aliases file 
        rcfg      -->    opens raspberry's configuration 
        gitota    -->    clones OTA repository
        otacfg    -->    opens updater conf. file
        otacpcfg  -->    copies ota conf. file.
        home      -->    go to the home directory (without '~' sign)\n
                        {endc}
        Do you want to use above aliases in your system?
        Reboot should be performed after adding those""".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC)
    print(aliases)
    selection = input(f"\n\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
    if selection == 'y':
        if parser.getint('added_functions', 'aliases_1'):
            print("\n\n\t\tLooks like you already have aliases added. \n\t\tDo you want to continue anyway?\n")
            selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
            if selection == 'y':
                aliases_content()
            if selection == 'a':
                features_menu(parser, config)
            else:
                aliases_menu(parser, config)
        else:
            aliases_content()
    if selection == 'a':
        features_menu(parser, config)
    else:
        aliases_menu(parser, config)


def self_updater(parser, config):
    def add_updater():
        clear_the_screen()
        logo_top(config.debug_mode)
        print("""
    Permissions required so 'zip' and 'unzip' program can be downloaded.
    Performed only during first instance of entering this sub-menu\n""")
        sleep(2)
        os.system("sudo echo")
        os.system("sudo apt install zip unzip")
        os.system("echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && \
         python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null")
        os.system("echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python \
         ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null")
        parser.set('added_functions', 'updater_planted', '1')
        parser_write(parser, config)

    if not parser.getint('added_functions', 'updater_planted'):
        add_updater()
    clear_the_screen()
    logo_top(config.debug_mode)
    updater = """{bold}
    If you want to update this program and download new firmware, 
    prepared for Arduino nodes - so you can next flash them 
    - you can just hit 'u' now. You can also type 'updateupdater'
    or 'uu' in the terminal window.
    Version of the updater is related to {blue}nodes firmware API number{endc},
          {bold}
    so you always know what firmware version updater contains.
    For example "2.2.5c" contains nodes firmware with "API level 22".
    Self-updater will test your internet connection during every update.
    Updating script is currently set to mode: {green}{update_mode}{endc}.\n\n
    """.format(green=Bcolors.GREEN, endc=Bcolors.ENDC, bold=Bcolors.BOLD, blue=Bcolors.BLUE,
               update_mode=config.update_mode)
    print(updater)
    print(f"{Bcolors.GREEN}\t\tUpdate now by pressing 'u'{Bcolors.ENDC}\n")
    print(f"{Bcolors.YELLOW}\t\tGo back by pressing 'b'{Bcolors.ENDC}\n\n")
    selection = input()
    if selection == 'b':
        features_menu(parser, config)
    if selection == 'u':
        os.system(". ./open_scripts.sh; updater_from_ota")
    else:
        self_updater(parser, config)


def features_menu(parser, config):
    clear_the_screen()
    logo_top(config.debug_mode)
    # todo "install avrdude" is obsolete cause it is now implemented in ota.sh

    features_menu_content = """

                    {red}{bold}{underline}FEATURES MENU{endc}{blue}{bold}

         
                        1 - Install AVRDUDE
                        
                        2 - Enable serial protocol {endc}{bold}
                        
                        3 - Access Point and Internet 
                        
                        4 - Show actual Pi's GPIO
                        
                        5 - Useful aliases
                        
                        6 - Update OTA software {endc}{yellow}{bold}
                            
                        e - Exit to main menu {endc}

             """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                        blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S)
    print(features_menu_content)
    selection = input()
    if selection == '1':
        avr_dude(config)
    if selection == '2':
        serial_menu(parser, config)
    if selection == '3':
        os.system("python3 ./net_and_ap.py")
    if selection == '4':
        if not parser.getint('added_functions', 'pinout_installed'):
            print("Some additional software has to be added so action can be performed. Ok?\n[yes/no]\n")
            while True:
                selection = input()
                if selection == 'y' or selection == 'yes':
                    if not os.system("sudo apt-get install python3-gpiozero"):
                        parser.set('added_functions', 'pinout_installed', '1')
                        parser_write(parser, config)
                        break
                    else:
                        print("\nFailed to install required package.\n")
                        sleep(2)
                        break
                if selection == 'n' or selection == 'no':
                    break
                else:
                    continue
        if parser.getint('added_functions', 'pinout_installed'):
            os.system("pinout")
            selection = input("\nDone? Hit 'Enter'\n")
        else:
            print("\nAdditional software needed. Please re-enter this menu.\n")
            sleep(3)
    if selection == '5':
        aliases_menu(parser, config)
    if selection == '6':
        self_updater(parser, config)
    if selection == 'e':
        main_menu(parser, config)
    else:
        features_menu(parser, config)


def first_time(parser, config):
    def update_notes():
        clear_the_screen()
        os.system("less ./docs/update-notes.txt")

    def second_page():
        clear_the_screen()
        welcome_second_page = """
                {bold}{underline}       CONFIGURATION PROCESS       {endc}

        {bold} 
        Software configuration process can be assisted with a wizard. 
        You have to enter point 5. of Main Menu and apply right values.
        It will configure this software, not RotorHazard server itself. 
        Thing like amount of used LEDs or password to admin page of RotorHazard
        should be configured separately - check RotorHazard Manager in Main Menu.


        Possible RotorHazard server versions:

        > {blue}'stable'{endc}{bold}- last stable release (can be from before few days or few months){endc}
        
        > {blue}'beta'  {endc}{bold}- last 'beta' release (usually has about few weeks, quite stable){endc}
        
        > {blue}'master'{endc}{bold}- absolutely newest features implemented (even if not well tested){endc}  
            """.format(bold=Bcolors.BOLD, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                       blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, orange=Bcolors.ORANGE_S)
        print(welcome_second_page)
        print(f"\n\n\t'f' - first page'{Bcolors.GREEN}\t'u' - update notes'{Bcolors.ENDC}\
            {Bcolors.YELLOW}\t'b' - back to menu{Bcolors.ENDC}\n\n")
        selection = input()
        if selection == 'f':
            first_page()
        if selection == 'b':
            main_menu(parser, config)
        if selection == 'u':
            update_notes()
        else:
            second_page()

    def first_page():
        clear_the_screen()
        welcome_first_page = """{bold}  

        You can use all implemented features, but if you want to be able to program
        Arduino-based nodes - enter Features menu and begin with first 2 points.

        Also remember about setting up config file - check second page.  

        This program has ability to perform 'self-updates' - in "Features Menu".

        More info about whole poject that this software is a part of: 
        https://www.instructables.com/id/RotorHazard-Updater/
        and in how_to folder - look for PDF file.
        New features and changes - see update notes section.
        If you found any bug - please report via GitHub or Facebook.
                Enjoy!
                                                Szafran
        {endc}""".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC)
        print(welcome_first_page)
        welcome_first_page_menu = """{green}
            s - second page {endc}
        
            u -  update notes {yellow}
        
            b - back to main menu {endc}
        """.format(green=Bcolors.GREEN, endc=Bcolors.ENDC, yellow=Bcolors.YELLOW)
        print(welcome_first_page_menu)
        selection = input()
        if selection == 's':
            second_page()
        if selection == 'u':
            update_notes()
        if selection == 'b':
            main_menu(parser, config)
        else:
            first_page()

    first_page()


def end(parser, config):
    parser_write(parser, config)
    clear_the_screen()
    print("\n\n")
    ota_image()
    print(f"\t\t\t\t\t{Bcolors.BOLD}Happy flyin'!{Bcolors.ENDC}\n")
    sleep(1.3)
    clear_the_screen()
    sys.exit()


def main_menu(parser, config):
    clear_the_screen()
    logo_top(config.debug_mode)
    config_check()
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        main_menu_content = """
        
                    {red}{bold}{underline}MAIN MENU{endc}{blue}{bold}
                    
                             
                        1 - RotorHazard Manager
                            
                        2 - Nodes flash and update {endc}{bold}
                            
                        3 - Start the server now
                            
                        4 - Additional features
                            
                        5 - Info + first time here
                            
                        6 - Configuration wizard {endc}{yellow}
                            
                        e - Exit {endc}
                            
                """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                           blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S)
        print(main_menu_content)
        selection = input()
        if selection == '1':
            os.system("python3 ./rpi_update.py")  # opens raspberry updating file
        if selection == '2':
            os.system("python3 ./nodes_update.py")  # opens nodes updating file
        if selection == '3':
            clear_the_screen()
            os.system(". ./open_scripts.sh; server_start")
        if selection == '4':
            features_menu(parser, config)
        if selection == '5':
            first_time(parser, config)
        if selection == '6':
            os.system(". ./open_scripts.sh; ota_configuration_start")
        if selection == 'logme':
            log_to_dev(parser, config)
        if selection == 'e':
            end(parser, config)


def main():
    updater_version = '2.2.10beta2f'
    '''
    version of THIS program - has nothing to do with the RH version
    it refers to the API level of newest contained nodes firmware
    third number refers to actual version of the updater itself
    '''
    home_dir = os.path.expanduser('~')
    clear_the_screen()
    print("\n\n")
    ota_image()
    config_check()
    parser, config = load_config()
    compatibility(parser, home_dir)
    if not os.path.exists(f"{home_dir}/.ota_markers/ota_config.txt"):
        os.system(f"cp {home_dir}/RH-ota/resources/ota_config.txt \
        {home_dir}/.ota_markers/ota_config.txt")
    first(parser, config, updater_version)
    main_menu(parser, config)


if __name__ == "__main__":
    main()
