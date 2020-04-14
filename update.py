import os
import sys
from time import sleep

from conf_wizard_net import conf_wizard_net
from conf_wizard_ota import conf_ota
from modules import clear_the_screen, Bcolors, logo_top, image_show, ota_image, load_config, load_ota_sys_markers, \
    write_ota_sys_markers, get_ota_version, server_start
# from net_and_ap import net_and_ap_conf
from rpi_update import main_window as rpi_update
from nodes_flash import flashing_menu
from nodes_update_old import nodes_update as old_flash_gpio


def compatibility():  # adds compatibility and fixes with previous versions
    from prev_comp import main as prev_comp
    prev_comp()


def config_check():
    if not os.path.exists("./updater-config.json"):
        prompt = """

          {prompt}  Looks that you haven't set up config file yet.     {endc}
          {prompt}  Please read about configuration process - point 5  {endc}
          {prompt}  and next enter configuration wizard - point 6.     {endc}
""".format(prompt=Bcolors.PROMPT, endc=Bcolors.ENDC)
        print(prompt)
        return False
    else:
        return True


def read_aliases_file():
    aliases_to_show = []
    with open('./resources/aliases.txt', 'r') as aliases_file:
        for line in aliases_file:
            if 'alias ' in line and '###' not in line:
                line = line.replace('alias ', '')
                line = line[0:line.index('=')] + ' ' + line[line.index('#'):-1]
                line = line.replace('#', '\t\t\t')
                aliases_to_show.append(line)
            elif '#' in line and '###' not in line:
                line = line.replace('#', '')
                aliases_to_show.append(line)
            elif '###' not in line:
                aliases_to_show.append(line)

    aliases_to_show = ('\n\t\t'.join(aliases_to_show))

    return aliases_to_show


def log_to_dev(config):
    log_write(config)
    log_send(config)


def log_write(config):
    os.system(f"./scripts/log_write.sh {config.user}")


def log_send(config):
    while True:
        selection = input("\n\n\tDo you want to send a log file for a review to the developer? [y/n] ")
        if selection == 'y' or selection == 'yes':
            log_name = input("\n\tPlease enter your name so we know who sent a log file: ")
            os.system(f"./scripts/log_send.sh {config.user} {log_name}")
            f = open("./log_data/log_code.txt", "r")
            code = ''
            for line in f:
                code = line
            code_error_msg = """
                -- Error occurred --
                
        Please send log file manually - from 'log_data' folder. 
        Uploading to server process has failed.
            """
            code_report = f"""
User code: {code}

------------------------------

"""
            print(code_report) if code != '' else print(code_error_msg)
        if selection == 'n' or selection == 'no':
            print("\n\nOK - your log file is stored as 'log.txt' in RH-ota/log_data/ directory.")
        input("\nHit 'Enter' to continue\n\n")
        if not os.system("cowsay You are awesome! Fly safe."):
            sleep(3)
        break


def updated_check(config):
    while os.path.exists(f"/home/{config.user}/.ota_markers/.was_updated"):
        clear_the_screen()
        logo_top(config.debug_mode)
        print("""\n\n {bold}
        
        Software was updated recently to the new version.

        You can read update notes now.


         {endc}  {green} 
            r - Read update notes {endc}{yellow}

            s - Skip and don't show again{endc}
            """.format(bold=Bcolors.BOLD_S, endc=Bcolors.ENDC,
                       green=Bcolors.GREEN, yellow=Bcolors.YELLOW))
        selection = input()
        if selection == 'r':
            os.system("less ./docs/update-notes.txt")
            os.system(f"rm /home/{config.user}/.ota_markers/.was_updated >/dev/null 2>&1")
            break
        if selection == 's':
            os.system(f"rm /home/{config.user}/.ota_markers/.was_updated >/dev/null 2>&1")
            break


def welcome_screen(updater_version):
    clear_the_screen()
    print("\n\n")
    image_show()
    print(f"\t\t\t{Bcolors.BOLD} Updater version: {str(updater_version)}{Bcolors.ENDC}")
    sleep(1)


def serial_menu(config):
    ota_status = load_ota_sys_markers(config.user)

    def uart_enabling():
        # TODO Make this repeatable without adding multiple copies at the end of config.txt.
        # P.F.: I added this to be performed when entering nodes flashing for the first time
        os.system("./scripts/sys_conf.sh uart")
        ota_status.uart_support_added = True
        write_ota_sys_markers(ota_status, config.user)
        print("""
        
        Serial port enabled successfully.
        You have to reboot Raspberry now,
        so changes would be implemented. Ok?
        
        
        
        r - Reboot now{yellow}
        
        e - Exit{endc}
            """.format(endc=Bcolors.ENDC, yellow=Bcolors.YELLOW_S))
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        if selection == 'e':
            return

    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        serial_adding_menu = """
            Serial port (UART) has to be enabled. 
            Without it Arduino-nodes cannot be programmed.
            Do you want to enable it now?
            
            
     {green}y - for yes {endc}
            
    {yellow}a - for abort{endc}
            """.format(yellow=Bcolors.YELLOW, green=Bcolors.GREEN, endc=Bcolors.ENDC)
        selection = input(serial_adding_menu)
        if selection == 'y':
            if ota_status.uart_support_added:
                print("\n\n\t\tLooks like you already enabled Serial port. \n\t\tDo you want to continue anyway?\n")
                selection = input(f"\t\t\t{Bcolors.YELLOW}Press 'y' for yes or 'a' for abort{Bcolors.ENDC}\n")
                if selection == 'y':
                    uart_enabling()
                    break
                if selection == 'a':
                    break
            else:
                uart_enabling()
                break
        if selection == 'a':
            break


def aliases_menu(config):
    ota_status = load_ota_sys_markers(config.user)

    def aliases_content():
        """load ota status, update aliases then write ota_status"""
        os.system("cat ./resources/aliases.txt | tee -a ~/.bashrc")
        ota_status.aliases_implemented = True
        write_ota_sys_markers(ota_status, config.user)
        print("\n\n\t\t    Aliases added successfully")
        sleep(2)
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
                print("""
                
            Looks like you already have aliases added. 
            Do you want to continue anyway?
        
        """)
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
    def check_if_beta_user(config):
        if config.beta_tester:
            updater_info = f'{Bcolors.RED}' \
                           f'Beta-tester mode is enabled - update will contain OTA in beta version.{Bcolors.ENDC}\n'
        else:
            updater_info = ''

        return updater_info

    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        updater = """{bold}
        You can update OTA software by hitting 'u' now. It is advised step 
        before updating the RotorHazard server or before flashing nodes,
        so you can be sure you use the newest possible software.
        
        OTA version number is related to {blue}nodes firmware API number{endc}{bold},
        so you always know what firmware version given OTA release contains.
        For example "2.2.5c" contains nodes firmware with "API level 22".
        
        Self-updater will test your internet connection before every update
        and prevent update if there is no internet connection established.
        
        {updater_info}
        
            {green}u - Update OTA now{endc}
        
           {yellow}e - Exit to main menu{endc}
        """.format(green=Bcolors.GREEN_S, endc=Bcolors.ENDC, bold=Bcolors.BOLD, blue=Bcolors.BLUE,
                   yellow=Bcolors.YELLOW_S, updater_info=check_if_beta_user(config))
        print(updater)
        selection = input()
        if selection == 'e':
            break
        if selection == 'u':
            os.system(". ./scripts/updater_from_ota.sh")


def features_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        features_menu_content = """
    
                                {rmf}FEATURES MENU{endc}{blue}{bold}
    
             
                        1 - Enable serial protocol {endc}{bold}
                        
                        2 - Access Point and Internet 
                        
                        3 - Show actual Pi's GPIO
                        
                        4 - Useful aliases
                        
                        5 - Update OTA software {endc}{bold}
                        
                        6 - Create a log file{yellow}
                            
                        e - Exit to main menu {endc}
    
                 """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                            blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, rmf=Bcolors.RED_MENU_HEADER)
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
        if selection == '6':
            log_to_dev(config)
        if selection == 'e':
            break


def first_time():
    def show_update_notes():
        clear_the_screen()
        os.system("less ./docs/update-notes.txt")

    def second_page():
        while True:
            clear_the_screen()
            welcome_second_page = """
                        {bold}{underline}CONFIGURATION PROCESS{endc}

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
            
        
            f - First page'         u - Update notes' {yellow}   e - Exit to menu{endc}
                  
            """.format(bold=Bcolors.BOLD, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC,
                       blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S,
                       orange=Bcolors.ORANGE_S)
            print(welcome_second_page)
            selection = input()
            if selection == 'f':
                return False  # go back to first page
            if selection == 'e':
                return True  # go back to main menu
            if selection == 'u':
                show_update_notes()

    def first_page():
        while True:
            clear_the_screen()
            welcome_first_page = """{bold}  
    
        You can use all implemented features, but if you want to be able to flash
        Arduino-nodes, you have to use official PCB or have 'hardware mod" done.

        Please remember about setting up config file - check out second page.  

        This program has ability to perform 'self-updates' - in "Features Menu".

        More info about whole poject that this software is a part of: 
        https://www.instructables.com/id/RotorHazard-Updater/
        and in how_to folder - look for PDF file.
        
        New features and changes - see update notes section.
        If you found any bug - please report via GitHub or Facebook.
        
                Enjoy!
                                                Szafran
        
            {green}
        s - Second page {endc}        u - Update notes {yellow}e - Exit to main menu {endc}
            """.format(green=Bcolors.GREEN, endc=Bcolors.ENDC, yellow=Bcolors.YELLOW_S, bold=Bcolors.BOLD)
            print(welcome_first_page)
            selection = input()
            if selection == 's':
                go_back_again = second_page()
                if go_back_again:
                    break  # user wants to go back to main menu.
            if selection == 'u':
                show_update_notes()
            if selection == 'e':
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
        conf_color = Bcolors.GREEN if config_check() is False else ''
        main_menu_content = """
        
                                {rmf}MAIN MENU{endc}
                    
                           {blue}{bold}  
                        1 - RotorHazard Manager
                            
                        2 - Nodes flash and update {endc}{bold}
                            
                        3 - Start the server now
                            
                        4 - Additional features
                            
                        5 - Info + first time here{configured}
                            
                        6 - Configuration wizard {endc}{yellow}
                            
                        e - Exit {endc}
                            
                """.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC, green=Bcolors.GREEN,
                           blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, configured=conf_color,
                           rmf=Bcolors.RED_MENU_HEADER)
        print(main_menu_content)
        selection = input()
        if selection == '1':
            rpi_update(config)
        if selection == '2':
            ota_status = load_ota_sys_markers(config.user)
            if ota_status.uart_support_added:
                old_flash_gpio(config) if config.old_hw_mod else flashing_menu(config)
            # enters "old" flashing menu only when "old_hw_mod" is confirmed
            else:
                serial_menu(config)
        if selection == '3':
            server_start()
        if selection == '4':
            features_menu(config)
        if selection == '5':
            first_time()
        if selection == '6':
            config = conf_ota(config)
        if selection == 'e':
            end()


def main():
    compatibility()
    updater_version = get_ota_version(False)
    config = load_config()
    welcome_screen(updater_version)
    updated_check(config)
    main_menu(config)


if __name__ == "__main__":
    main()
