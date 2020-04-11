from time import sleep
import os
from types import SimpleNamespace
from modules import clear_the_screen, Bcolors, logo_top, write_json, load_config
from pathlib import Path

'''
Check if a config file already exists. if it does, 
ask the user if they want to overwrite it.
'''


def conf_check():
    conf_now_flag = 0
    if os.path.exists("./updater-config.json"):
        print("\n\tLooks that you have OTA software already configured.")
        valid_options_conf_check = ['y', 'yes', 'n', 'no']
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [yes/no]\t\t").strip()
            if cont_conf in valid_options_conf_check:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if cont_conf[0] == 'y': conf_now_flag = 1
        if cont_conf[0] == 'n': conf_now_flag = 0
    else: conf_now_flag = 1
    return conf_now_flag


def ask_custom_rh_version():
    while True:
        version = input(f"\nPlease enter the version tag that you wish to install [EG: 2.1.0-beta.3]:\t")
        confirm = input(f"""
            You entered: '{version}' 

            Confirm [yes/no]""")
        if confirm.upper().startswith('Y'):
            return version


def do_config(config):
    home_dir = str(Path.home())
    clear_the_screen()
    logo_top(False)

    # Always define variables before using them.
    conf_now_flag = conf_check()

    if conf_now_flag:
        config = SimpleNamespace()
        print("""
        
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.
""")
        pi_user_name = input("\nWhat is your user name on Raspberry Pi? [default: pi]\t\t\t")
        config.pi_user = pi_user_name
        while True:
            version = input(f"\nChoose RotorHazard version? \
[{Bcolors.UNDERLINE}stable{Bcolors.ENDC} | beta | master | custom]").lower()
            version_valid_options = ['master', 'stable', 'beta', 'custom']
            if version not in version_valid_options:
                print("\nPlease enter correct value!")
            else:
                config.rh_version = version
                # If the user specifies custom for version, re-ask the question
                # and ask exactly what version tag they want:
                if version == 'custom':
                    print("Support for custom versions of RH coming soon")
                    input("Press Enter")
                    continue  # todo add support for custom version of RotorHazard
                    # maybe sth like "check_if_rh_version_is_custom()" in nodes_update
                    # config.rh_version = ask_custom_rh_version()
                break

        while True:
            country_code = input("\nWhat is your country code? [default: GB]\t\t\t\t").upper()
            if 1 < len(country_code) <= 3:
                config.country = country_code
                break
            else: print("\nPlease enter correct value!")

        while True:
            nodes = input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
            if not nodes.isdigit() or int(nodes) > 8: print("\nPlease enter correct value!")
            else:
                config.nodes_number = int(nodes)
                break

        if int(nodes) % 2 != 0:
            while True:
                odd_nodes_note = """
Since you declared odd number of nodes, please input, 
which pin will be used as GPIO reset pin? 
[ default (used on official PCB): 17 ] \t\t\t\t\t"""
                gpio_reset_pin = input(odd_nodes_note)
                if int(gpio_reset_pin) > 40:
                    print("\nPlease enter correct value!")
                else:
                    config.gpio_reset_pin = int(gpio_reset_pin)
                    break
        elif int(nodes) % 2 == 0:
            gpio_reset_pin = False
            config.gpio_reset_pin = gpio_reset_pin

        while True:
            debug_mode = input("\nWill you use OTA software in a debug mode? [yes/no | default: no]\t").lower()
            debug_mode_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if debug_mode not in debug_mode_allowed_values: print("\nPlease enter correct value!")
            else:
                debug_mode_val = debug_mode in ['yes', '1', 'y']
                config.debug_mode = debug_mode_val
                break

        if debug_mode_val:
            debug_user = input("\nWhat is your user name on debugging OS? \t\t\t\t")
            config.debug_user = debug_user
        else: config.debug_user = 'racer'
        while True:
            old_hw_mod = input("""
Are you using older, non-i2c hardware flashing mod? 
(nodes reset pins connected to gpio pins) [ yes/no | default: no ]\t""").lower()[0]
            # honestly, we only care about the first letter.
            if old_hw_mod == "y":
                old_hw_mod, config.old_hw_mod = True, True
                break
            elif old_hw_mod == "n":
                old_hw_mod, config.old_hw_mod = False, False
                break
            else:
                print("\nPlease enter correct value!")
        while old_hw_mod:
            pins_assign = input("\nPins assignment? [default/custom/PCB | default: default]\t\t").lower()
            pins_valid_options = ['default', 'PCB', 'pcb', 'custom']
            if pins_assign not in pins_valid_options: print("\nPlease enter correct value!")
            else:
                config.pins_assignment = pins_assign
                break
        else: config.pins_assignment = 'default'

        while True:
            user_is_beta_tester = input("\nAre you a beta tester? [yes/no | default: no]\t\t\t\t")
            beta_tester_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if user_is_beta_tester not in beta_tester_allowed_values: print("\nPlease enter correct value!")
            else:
                config.beta_tester = user_is_beta_tester in ['yes', '1', 'y']
                break

        print(f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}:

        User name:              {config.pi_user}
        RotorHazard version:    {config.rh_version}
        Debug user name:        {config.debug_user}
        Country code:           {config.country}
        Nodes amount:           {config.nodes_number}
        Old hardware mod:       {config.old_hw_mod}    
        Debug mode:             {config.debug_mode}    
        Pins assignment:        {config.pins_assignment}
        GPIO reset pin:         {config.gpio_reset_pin}
        Beta tester:            {config.beta_tester}
         
        Please check. Confirm? [yes/change/abort]\n""")
        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip().lower()
            if selection in valid_options:
                break
            else: print("\ntoo big fingers :( wrong command. try again! :)")
        if selection == 'y' or selection == 'yes':
            write_json(config, f"{home_dir}/RH-ota/updater-config.json")
            # Once we write out the json config we should re-load it just
            # to ensure consistency.
            config = load_config()
            print("Configuration saved.\n")
            sleep(0.5)
            conf_now_flag = 0
        if selection in ['change', 'n', 'no']:
            conf_now_flag = 1
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            conf_now_flag = 0

    return conf_now_flag, config


def conf_ota(config):
    """
        repeat the configuration script until
        the user ether aborts, configures ota
        or it was already configured.
    :return:
    """
    config_now = 1
    while config_now:
        config_now, config = do_config(config)
    return config


def main():
    config = load_config()
    conf_ota(config)


if __name__ == "__main__":
    main()
