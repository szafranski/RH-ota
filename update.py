import os
import sys
from time import sleep

from conf_wizard_net import conf_wizard_net
from conf_wizard_ota import conf_ota
from modules import clear_the_screen, Bcolors, logo_top, image_show, ota_image, load_config, load_ota_config, \
    write_ota_config, get_ota_version
from net_and_ap import net_and_ap_conf
from rpi_update import main_window as rpi_update
from nodes_flash import flashing_menu
from nodes_update_old import nodes_update as old_flash_gpio


def compatibility():  # adds compatibility and fixes with previous versions
    from prev_comp import prev_comp
    prev_comp()


def config_check():
    if not os.path.exists("./updater-config.json"):
        print(f"""{Bcolors.BOLD}\
        Looks that you haven't set up config file yet.
        Please read about configuration process - point 5
        and next enter configuration wizard - point 6.\
        {Bcolors.ENDC}""")


def log_to_dev(config):
    log_write(config)
    log_send(config)


def read_aliases_file():  # todo almost done, readability has to be improved yet (remove "(...)" part from every line
    aliases_to_show = []
    with open('./resources/aliases.txt', 'r') as aliases_file:
        for line in aliases_file:
            if 'alias ' in line and '###' not in line:
                line = line.replace('alias ', '')
                aliases_to_show.append(line)
            elif '#' in line and '###' not in line:
                line = line.replace('#', '')
                aliases_to_show.append(line)
            elif '###' not in line:
                aliases_to_show.append(line)

    aliases_to_show = (''.join(aliases_to_show))

    return aliases_to_show


def log_write(config):
    os.system(f". ./scripts/log_write.sh {config.user}")


def log_send(config):
    while True:
        selection = input("\n\n\tDo you want to send a log file for a review to the developer? [y/n] ")
        if selection == 'y' or selection == 'yes':
            log_name = input("\n\tPlease enter your name so we know who sent a log file: ")
            os.system(f". ./scripts/log_send.sh {config.user} {log_name}")
            f = open("./log_data/log_code.txt", "r")
            code = ''
            for line in f:
                code = line
            short_line = "".center(30, "-")
            print(f"""\n
                User code: {code}\n
            {short_line}\n""")
            input("\n\nHit 'Enter' to continue\n\n")
            if not os.system("cowsay You are awesome! Fly safe."):
                sleep(3)
            break
        if selection == 'n' or selection == 'no':
            print("\n\n\tOK - you log file is stored under 'log.txt' name in RH-ota directory.")
            input("\n\n\tHit 'Enter' to continue\n\n")
            break


def updated_check(config):
    while True:
        if os.path.exists(f"/home/{config.user}/.ota_markers/.was_updated"):
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
                break
            if selection == 's':
                break
        else:
            break
        os.system(f"rm /home/{config.user}/.ota_markers/.was_updated >/dev/null 2>&1")


def welcome_screen(config, updater_version):
    clear_the_screen()
    print("\n\n")
    image_show()
    print(f"\t\t\t{Bcolors.BOLD} Updater version: {str(updater_version)}{Bcolors.ENDC}")
    sleep(1)
    updated_check(config)


def serial_menu(config):
    ota_status = load_ota_config(config.user)

    def serial_content():
        # TODO Make this repeatable without adding multiple copies at the end of config.txt.
        # P.F. or just make it as an automatic feature when opening nodes-flashing menu
        # for the first time
        os.system("echo 'enable_uart=1'| sudo tee -a /boot/config.txt")
        os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
        ota_status.uart_support_added = True
        write_ota_config(ota_status, config.user)
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
        serial_adding_menu = f"""
            Serial port has to be enabled. 
            Without it Arduinos cannot be programmed.
            Do you want to enable it now?
            
            {Bcolors.GREEN}
            y - for yes {Bcolors.ENDC}
            {Bcolors.YELLOW}
            a - for abort{Bcolors.ENDC}
            """
        selection = input(serial_adding_menu)
        if selection == 'y':
            if ota_status.uart_support_added:
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


def aliases_menu(config):
    ota_status = load_ota_config(config.user)

    def aliases_content():
        """load ota status, update aliases then write ota_status"""
        os.system("cat ./resources/aliases.txt | tee -a ~/.bashrc")
        ota_status.aliases_implemented = True
        write_ota_config(ota_status, config.user)
        print("\n\n\t\t    Aliases added successfully")
        sleep(3)
        return

    while True:
        clear_the_screen()
        aliases_description = f""" 
        Aliases in Linux act like shortcuts or references to another commands. 
        You can use them every time when you operates in the terminal window. 
        For example instead of typing 'python ~/RotorHazard/src/server/server.py' 
        you can just type 'ss' (server start) etc. Aliases can be modified and added 
        anytime you want. You just have to open '~./bashrc' file in text editor 
        - like 'nano'. After that you have reboot or type 'source ~/.bashrc'. 
        {Bcolors.BOLD}
        {read_aliases_file()}
        {Bcolors.ENDC}
            Do you want to use above aliases in your system?
            Reboot should be performed after adding those"""
        print(aliases_description)
        selection = input(f"\n\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
        if selection == 'y':
            if ota_status.aliases_implemented:
                print("\n\n\t\tLooks like you already have aliases added. \n\t\tDo you want to continue anyway?\n")
                selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
                if selection == 'y':
                    aliases_content()
                    break
                if selection == 'a':
                    return
            else:
                aliases_content()
                break
        if selection == 'a':
            return


def self_updater(config):
    ota_status = load_ota_config(config.user)

    def add_updater():
        clear_the_screen()
        logo_top(config.debug_mode)
        ota_status.updater_planted = True
        write_ota_config(ota_status, config.user)

    if not ota_status.updater_planted:
        add_updater()
    while True:
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
        Self-updater will test your internet connection during every update.\n\n
        """.format(green=Bcolors.GREEN, endc=Bcolors.ENDC, bold=Bcolors.BOLD, blue=Bcolors.BLUE)
        print(updater)
        print(f"{Bcolors.GREEN}\t\tUpdate now by pressing 'u'{Bcolors.ENDC}\n")
        print(f"{Bcolors.YELLOW}\t\tGo back by pressing 'b'{Bcolors.ENDC}\n\n")
        selection = input()
        if selection == 'b':
            break
        if selection == 'u':
            os.system(". ./scripts/updater_from_ota.sh")


def features_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        features_menu_content = """
    
                        {red}{bold}{underline}FEATURES MENU{endc}{blue}{bold}
    
             
                            1 - Enable serial protocol {endc}{bold}
                            
                            2 - Access Point and Internet 
                            
                            3 - Show actual Pi's GPIO
                            
                            4 - Useful aliases
                            
                            5 - Update OTA software {endc}{yellow}{bold}
                                
                            e - Exit to main menu {endc}
    
                 """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                            blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S)
        print(features_menu_content)
        selection = input()
        if selection == '1':
            serial_menu(config)
        if selection == '2':
            conf_wizard_net(config)
        if selection == '3':
            os.system("pinout")
            input("\nDone? Hit 'Enter'\n")
        if selection == '4':
            aliases_menu(config)
        if selection == '5':
            self_updater(config)
        if selection == 'e':
            break


def first_time():
    def update_notes():
        clear_the_screen()
        os.system("less ./docs/update-notes.txt")

    def second_page():
        while True:
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
                return False  # go back to first page
            if selection == 'b':
                return True  # go back to main menu
            if selection == 'u':
                update_notes()

    def first_page():
        while True:
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
                go_back_again = second_page()
                if go_back_again:  # user wants to go back to main menu.
                    break
            if selection == 'u':
                update_notes()
            if selection == 'b':
                break

    first_page()


def end():
    clear_the_screen()
    print("\n\n")
    ota_image()
    print(f"\t\t\t{Bcolors.BOLD}Happy flyin'!{Bcolors.ENDC}\n")
    sleep(1.3)
    clear_the_screen()
    sys.exit()


def main_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        config_check()
        main_menu_content = """
        
                    {red}{bold}{underline}MAIN MENU{endc}
                    
                           {blue}{bold}  
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
            rpi_update(config)
        if selection == '2':
            old_flash_gpio(config) if config.old_hw_mod else flashing_menu(config)
            # enters "old" flashing menu only when "old_hw_mod" is confirmed
        if selection == '3':
            clear_the_screen()
            os.system(". ./scripts/server_start.sh")
        if selection == '4':
            features_menu(config)
        if selection == '5':
            first_time()
        if selection == '6':
            config = conf_ota(config)
        if selection == 'logme':
            log_to_dev(config)
        if selection == 'e':
            end()


def main():
    compatibility()
    config = load_config()
    updater_version = get_ota_version(False)
    clear_the_screen()
    config_check()
    print("\n\n")
    welcome_screen(config, updater_version)
    main_menu(config)


if __name__ == "__main__":
    main()
