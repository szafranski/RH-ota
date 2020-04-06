import os
from pathlib import Path
from time import sleep
from conf_wizard_rh import conf_rh
from modules import clear_the_screen, Bcolors, image_show, internet_check, load_ota_config, write_ota_config, \
    load_config


def get_rotorhazard_server_version(user):
    server_py = Path(f"/home/{user}/RotorHazard/src/server/server.py")
    server_version_name = ''
    server_installed_flag = False
    if server_py.exists():
        with open(server_py, 'r') as open_file:
            for line in open_file:
                if line.startswith('RELEASE_VERSION'):
                    # RELEASE_VERSION = "2.2.0 (dev 1)" # Public release version code
                    server_version_name = line.strip().split('=')[1].strip()
                    server_version_name = server_version_name.strip().split('#')[0].replace('"', '')
                    server_version_name = f"{Bcolors.GREEN}{server_version_name}{Bcolors.ENDC} "
                    server_installed_flag = True
                    break
    else:
        server_version_name = f'{Bcolors.YELLOW}{Bcolors.UNDERLINE}installation not found{Bcolors.ENDC}'
        server_installed_flag = False
    return server_installed_flag, server_version_name


def check_rotorhazard_config_status(user):
    if os.path.exists(f"/home/{user}/RotorHazard/src/server/config.json"):
        config_soft = f"{Bcolors.GREEN}configured👍 {Bcolors.ENDC} "
        config_flag = True
    else:
        config_soft = f"{Bcolors.YELLOW}{Bcolors.UNDERLINE}not configured{Bcolors.ENDC}  👎"
        config_flag = False
    return config_soft, config_flag


def end_update(user, server_configured_flag, server_installed_flag):
    if not server_configured_flag and server_installed_flag:
        configure = f"{Bcolors.GREEN}'c' - configure RotorHazard now{Bcolors.ENDC}"
    else:
        configure = "'c' - reconfigure RotorHazard server"
    while True:
        print(f"""
                    {configure}
        
                    'r' - reboot - recommended when configured
                    
                    's' - start the server now{Bcolors.YELLOW}
                    
                    'e' - exit now{Bcolors.ENDC}""")
        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        if selection == 'e':
            return
        if selection == 'c':
            conf_rh()
        if selection == 's':
            clear_the_screen()
            os.chdir(f"/home/{user}/RH-ota")
            os.system("./scripts/server_start.sh")


def end_installation(user):
    while True:
        print(f"""
    
            {Bcolors.GREEN}
            'c' - configure the server now - recommended {Bcolors.ENDC}
            
            'r' - reboot - recommended after configuring
            
            's' - start the server now{Bcolors.YELLOW}
            
            'e' - exit now{Bcolors.ENDC}""")

        selection = input()
        if selection == 'r':
            os.system("sudo reboot")
        if selection == 'e':
            return
        if selection == 'c':
            conf_rh()
            break
        if selection == 's':
            clear_the_screen()
            os.chdir(f"/home/{user}/RH-ota")
            os.system("./scripts/server_start.sh")


def installation(conf_allowed, linux_testing, user, server_version):
    ota_config = load_ota_config(user)
    os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &") if not linux_testing else None
    clear_the_screen()
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Installation canceled.")
    else:
        print("\nInternet connection - OK")
        sleep(2)
        clear_the_screen()
        print(f"{Bcolors.BOLD}Installation process has been started - please wait...{Bcolors.ENDC}")
        installation_completed = """
        
        
            #####################################################
            ##                                                 ##
            ##{bold}{green}Installation completed{thumbs}{endc}##
            ##                                                 ##
            #####################################################


        After rebooting please check by typing 'sudo raspi-config' 
        if I2C, SPI and SSH protocols are active.
                    """.format(thumbs="👍👍👍  ", bold=Bcolors.BOLD_S,
                               endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)

        os.system(f"./scripts/install_rh.sh {user} {server_version}")
        input("press Enter to continue.")
        os.system("sh. ./scripts/sys_conf.sh") if conf_allowed else None
        ota_config.rh_installation_done = True
        write_ota_config(ota_config, user)
        print(installation_completed)
        end_installation(user)


def update(linux_testing, user, server_version):
    os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &") if not linux_testing else None
    internet_flag = internet_check()
    if not internet_flag:
        print("\nLooks like you don't have internet connection. Update canceled.")
        sleep(2)
    else:
        print("\nInternet connection - OK")
        sleep(2)
        clear_the_screen()
        if not os.path.exists(f"/home/{user}/RotorHazard"):
            print(f"""{Bcolors.BOLD}
    Looks like you don't have RotorHazard server software installed for now. \n\t\t
    If so please install your server software first or you won't be able to use the timer.{Bcolors.ENDC}""")
            print(f"""\n\n{Bcolors.GREEN} 
        'i' - Install the software - recommended{Bcolors.ENDC}\n 
        'a' - Abort both  \n\n{Bcolors.ENDC}""")
            selection = input()
            if selection == 'i':
                conf_allowed = True
                installation(conf_allowed, linux_testing, user, server_version)
            if selection == 'a':
                clear_the_screen()
                return
            else:
                return
        else:
            clear_the_screen()
            print(f"\n\t{Bcolors.BOLD}Updating existing installation - please wait...{Bcolors.ENDC} \n")
            update_completed = """\n\n\t
                ################################################
                ##                                            ##
                ##{bold}{green}Update completed!{thumbs}{endc}##
                ##                                            ##
                ################################################
                        """.format(thumbs="👍👍👍  ", bold=Bcolors.BOLD_S,
                                   endc=Bcolors.ENDC_S, green=Bcolors.GREEN_S)
            os.system(f"./scripts/update_rh.sh {user} {server_version}")
            print(update_completed)
            config_flag, config_soft = check_rotorhazard_config_status(user)
            server_installed_flag, server_version_name = get_rotorhazard_server_version(user)
            end_update(user, config_flag, server_installed_flag)


def main_window(config):

    user = config.user

    while True:
        rh_config_text, rh_config_flag = check_rotorhazard_config_status(config.user)
        clear_the_screen()
        server_installed_flag, server_version_name = get_rotorhazard_server_version(config.user)
        ota_config = load_ota_config(user)
        sleep(0.1)
        welcome_text = """
            \n\n{red} {bold}
            AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE
                {endc}{bold}
            You can automatically install and update RotorHazard timing software. 
            Additional dependencies and libraries also will be installed or updated.
            Current database, configs and custom bitmaps will stay on their place.
            Source of the software is set to {underline}{blue}{server_version}{endc}{bold} version from the official 
            RotorHazard repository.
             
            Perform self-updating of this software, before updating server software.
            Also make sure that you are logged as user {underline}{blue}{user}{endc}{bold}.
            
            You can change those in configuration wizard in Main Menu.
            
            Server installed right now: {server} {bold}
            
            RotorHazard configuration state: {config_soft}
            """.format(bold=Bcolors.BOLD, underline=Bcolors.UNDERLINE, endc=Bcolors.ENDC, blue=Bcolors.BLUE,
                       yellow=Bcolors.YELLOW, red=Bcolors.RED, orange=Bcolors.ORANGE, server_version=config.RH_version,
                       user=user, config_soft=rh_config_text, server=server_version_name)
        print(welcome_text)

        if not rh_config_flag:
            configure = f"{Bcolors.GREEN}'c' - Configure RotorHazard server{Bcolors.ENDC}"
        else:
            configure = "'c' - Reconfigure RotorHazard server"
        if not server_installed_flag:
            install = f"{Bcolors.GREEN}'i' - Install software from scratch{Bcolors.ENDC}"
        else:
            install = """'i' - Install software from scratch"""
        print("""
                    {install}
                    
                    {configure}
                    
                    'u' - Update existing installation {yellow}
                        
                    'e' - Exit to Main Menu{endc}
                    
                """.format(yellow=Bcolors.YELLOW, endc=Bcolors.ENDC, configure=configure, install=install))
        selection = input()
        if selection == 'c':
            if not server_installed_flag:
                print("Please install before configuring.")
            else:
                conf_rh()
        if selection == 'i':
            if ota_config.rh_installation_done:
                clear_the_screen()
                already_installed_prompt = """
                {bold}
        Looks like you already have RotorHazard server installed
        (or at least that your system was once configured).{endc}
        
        If that's the case please use {underline} update mode {endc} - 'u'
        or force installation {underline} without {endc} sys. config. - 'i'.
                
                {green} 
            'u' - Select update mode - recommended {endc}\n 
            'i' - Force installation without sys. config.\n
            'c' - Force installation and sys. config.\n {yellow}
            'a' - Abort both  \n {endc}""".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE,
                                                  yellow=Bcolors.YELLOW, green=Bcolors.GREEN)
                print(already_installed_prompt)
                selection = input()
                if selection == 'u':
                    update(config.debug_mode, config.user, config.server_version)
                if selection == 'i':
                    conf_allowed = False
                    installation(conf_allowed, config.debug_mode, config.user, config.server_version)
                if selection == 'c':
                    confirm_valid_options = ['y', 'yes', 'n', 'no', 'abort', 'a']
                    while True:
                        confirm = input("\n\t\tAre you sure? [yes/abort]\t").strip()
                        if confirm in confirm_valid_options:
                            break
                        else:
                            print("\ntoo big fingers :( wrong command. try again! :)")
                    if confirm == 'y' or confirm == 'yes':
                        conf_allowed = True
                        installation(conf_allowed, config.debug_mode, config.user, config.server_version)
                    if confirm in ['n', 'no', 'abort', 'a']:
                        pass
                if selection == 'a':
                    clear_the_screen()
                    image_show()
                    sleep(0.5)
                    break
            else:
                conf_allowed = True
                installation(conf_allowed, config.debug_mode, config.user, config.server_version)
        if selection == 'u':
            update(config.debug_mode, config.user, config.RH_version)
        if selection == 'e':
            clear_the_screen()
            os.chdir(f"/home/{config.user}/RH-ota")
            image_show()
            sleep(0.3)
            break


def rpi_update(config):

    main_window(config)


def main():
    config = load_config()
    rpi_update(config)


if __name__ == "__main__":
    main()
