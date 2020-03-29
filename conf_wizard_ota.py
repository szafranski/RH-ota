from time import sleep
import os
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
        if cont_conf[0] == 'y':
            conf_now_flag = 1
        if cont_conf[0] == 'n':
            conf_now_flag = 0
            breakpoint()
    else:
        conf_now_flag = 1
    return conf_now_flag


def do_config(config):
    home_dir = str(Path.home())
    clear_the_screen()
    logo_top(False)

    # Always define variables before using them.

    conf_now_flag = conf_check()

    if conf_now_flag:

        print("""\n
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.\n""")
        pi_user_name = input("\nWhat is your user name on Raspberry Pi? [default: pi]\t\t\t")
        config.pi_user = pi_user_name
        while True:
            version = input(f"\nWhat RotorHazard version will you use? \
[{Bcolors.UNDERLINE}stable{Bcolors.ENDC} | beta | master]\t\t")
            version_valid_options = ['master', 'stable', 'beta']
            if version not in version_valid_options:
                print("\nPlease enter correct value!")
            else:
                config.RH_version = version
                break

        debug_user = input("\nWhat is your user name on debugging OS? [default: racer]\t\t")
        config.debug_user = debug_user

        country_code = input("\nWhat is your country code? [default: GB]\t\t\t\t")
        config.country = country_code

        while True:
            nodes = input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
            if not nodes.isdigit() or int(nodes) > 8:
                print("\nPlease enter correct value!")
            else:
                config.nodes_number = nodes
                break

        while True:
            debug_mode = input("\nWill you use \"OTA\" software in a debug mode? [yes/no | default: no]\t")
            debug_mode_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if debug_mode not in debug_mode_allowed_values:
                print("\nPlease enter correct value!")
            else:
                debug_mode_val = False
                if debug_mode in ['yes', '1', 'y']:
                    debug_mode_val = True
                elif debug_mode in ['no', '0', 'n']:
                    debug_mode_val = False
                config.debug_mode = debug_mode_val
                break
        while True:
            pins_assign = input("\nPins assignment? [default/custom/PCB | default: default]\t\t")
            pins_valid_options = ['default', 'PCB', 'pcb', 'custom']
            if pins_assign not in pins_valid_options:
                print("\nPlease enter correct value!")
            else:
                config.pins_assignment = pins_assign
                break

        while True:
            no_pdf = input("\nUpdates without PDF? [yes/no | default: yes]\t\t\t\t")
            no_pdf_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if no_pdf not in no_pdf_allowed_values:
                print("\nPlease enter correct value!")
            else:
                no_pdf_val = False
                if no_pdf in ['yes', '1', 'y']:
                    no_pdf_val = True
                elif no_pdf in ['no', '0', 'n']:
                    no_pdf_val = False
                config.updates_without_pdf = no_pdf_val
                break

        while True:
            bool_gpio_reset_pin = input("\nWill you use odd number of nodes? [ yes/no | default: no ]\t\t")
            bool_gpio_reset_pin_allowed_values = ['yes', 'no', '0', '1', 'y', 'n']
            if bool_gpio_reset_pin not in bool_gpio_reset_pin_allowed_values:
                print("\nPlease enter correct value!")
            else:
                if bool_gpio_reset_pin in ['yes', '1', 'y']:
                    while True:
                        gpio_reset_pin = input("\nWhat pin will be used as GPIO reset? [ default (PCB): 17 ]\t\t")
                        if int(gpio_reset_pin) > 40:
                            print("\nPlease enter correct value!")
                        else:
                            config.gpio_reset = int(gpio_reset_pin)
                            break
                else:
                    gpio_reset_pin = False
                config.gpio_reset_pin = gpio_reset_pin
                break  # todo - it works but weird configuration in json occures - see GH issue

        while True:
            pi_4_owner = input("\nAre you using Raspberry Pi 4? [yes/no | default: no]\t\t\t")
            pi_4_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if pi_4_owner not in pi_4_allowed_values:
                print("\nPlease enter correct value!")
            else:
                pi_4_val = False
                if pi_4_owner in ['yes', '1', 'y']:
                    pi_4_val = True
                elif pi_4_owner in ['no', '0', 'n']:
                    pi_4_val = False
                config.pi_4_cfg = pi_4_val
                break

        while True:
            user_is_beta_tester = input("\nAre you a beta tester? [yes/no | default: no]\t\t\t\t")
            beta_tester_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
            if user_is_beta_tester not in beta_tester_allowed_values:
                print("\nPlease enter correct value!")
            else:
                beta_tester_val = False
                if user_is_beta_tester in ['yes', '1', 'y']:
                    beta_tester_val = True
                elif user_is_beta_tester in ['no', '0', 'n']:
                    beta_tester_val = False
                config.beta_tester = beta_tester_val
                break

        print(f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}:

        User name:              {config.pi_user}
        RotorHazard version:    {config.RH_version}
        Debug user name:        {config.debug_user}
        Country code:           {config.country}
        Nodes amount:           {config.nodes_number}
        Debug mode:             {config.debug_mode}    
        Pins assignment:        {config.pins_assignment}
        Updates without PDF:    {config.updates_without_pdf}
        GPIO reset pin:         {config.gpio_reset}
        Pi 4 user:              {config.pi_4_cfg}
        Beta tester:            {config.beta_tester}
         
        Please check. Confirm? [yes/change/abort]\n""")
        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if selection == 'y' or selection == 'yes':
            write_json(config, f"{home_dir}/RH-ota/updater-config.json")
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
