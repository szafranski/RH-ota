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
    conf_now_flag = 1
    if os.path.exists("./updater-config.json"):
        print("\n\tYou have already configured the Install Manager.")
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [Y/n]\t\t")
            if not cont_conf:
                print("answer defaulted to: yes")
                break
            elif cont_conf[0].lower() == 'y':
                conf_now_flag = True
                break
            elif cont_conf[0] == 'n':
                conf_now_flag = False
                break
            else:
                print("\nPlease enter a valid selection")

    return conf_now_flag


def ask_custom_rh_version():
    while True:
        version = input("\nPlease enter the version tag that you wish to install [e.g. 2.1.0-beta.3]:\n")
        print("Firmware available to flash will be defaulted to 'stable' version.\n")
        custom_confirm = input(f"""
            You entered version: '{version}' 

            Confirm [Y/n]       """)
        if custom_confirm.lower() == 'y' or not custom_confirm:
            return version


def do_config(old_config):
    home_dir = str(Path.home())
    clear_the_screen()
    logo_top(False)

    # Always define variables before using them.
    conf_now_flag = conf_check()

    if conf_now_flag:
        config = SimpleNamespace()
        print("""
        
Please type your configuration data. It can be modified later.
If you want to use value given as default, press 'Enter'.
""")
        pi_user_name = input("\nWhat is your user name on the Raspberry Pi? [default: pi]\t\t")
        if not pi_user_name:
            config.pi_user = 'pi'
            print("defaulted to: 'pi'")
        else:
            config.pi_user = pi_user_name
        while True:
            version = input(f"\nChoose RotorHazard version? \
[{Bcolors.UNDERLINE}stable{Bcolors.ENDC} | beta | main]\t\t\t").lower()
            if not version:
                config.rh_version = 'stable'
                print("defaulted to: 'stable'")
                break
            elif version in ['main', 'stable', 'beta']:
                config.rh_version = version
                break
            elif version == 'custom':
                # custom - hidden option, just for developers and testing.
                # Nodes flashing will be defaulted to stable in that case
                # If the user specifies custom for version, re-ask the question
                # and ask exactly what version tag they want:
                config.rh_version = ask_custom_rh_version()
                break
            else:
                print("\nPlease enter a valid selection")

        while True:
            country_code = input("\nWhat is your country code? [default: GB]\t\t\t\t").upper()
            if not country_code:
                config.country = 'GB'
                print("defaulted to: 'GB'")
                break
            elif len(country_code) < 4:
                config.country = country_code
                break
            else:
                print("\nPlease enter a valid selection")

        while True:
            nodes_number = input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
            if not nodes_number.isdigit() or int(nodes_number) > 8:
                print("\nPlease enter correct value!")
            else:
                config.nodes_number = int(nodes_number)
                break

        if int(nodes_number) % 2 != 0:
            while True:
                odd_nodes_note = """
Since you declared an odd number of nodes,
which pin will be used as the GPIO reset pin?
[ default (used on official PCB): 17 ] \t\t\t\t\t"""
                gpio_reset_pin = input(odd_nodes_note)
                if not gpio_reset_pin:
                    config.gpio_reset_pin = 17
                    print("defaulted to: 17")
                    break
                elif int(gpio_reset_pin) < 40:
                    config.gpio_reset_pin = int(gpio_reset_pin)
                    break
                else:
                    print("\nPlease enter correct value!")
        else:
            config.gpio_reset_pin = False

        while True:
            flashing_port_name = input("""
What port will be used for flashing Arduinos?
Usually 'ttyS0' or 'ttyAMA0' (on older OSes) [default: ttyS0]\t\t""")
            if not flashing_port_name:
                config.port_name = 'ttyS0'
                print("defaulted to 'ttyS0'")
                break
            else:
                config.port_name = flashing_port_name
                break
        print("\nDo you want to enter advanced configuration? [y/N]")
        while True:
            advanced_wizard_flag = input("\t").strip().lower()
            if not advanced_wizard_flag:
                print("defaulted to: no")
                advanced_wizard_flag = False
                break
            elif advanced_wizard_flag[0] == 'y':
                advanced_wizard_flag = True
                break
            elif advanced_wizard_flag[0] == 'n':
                advanced_wizard_flag = False
                break
            else:
                print("\nPlease enter a valid selection")

        if advanced_wizard_flag:

            while True:
                bus_number = input("""
What is the number of the I2C bus used with nodes? [0/1 | default: 1]\t""")
                if not bus_number:
                    bus_number, config.i2c_bus_number = 1, 1
                    print("defaulted to: 1")
                    break
                elif bus_number.isdigit():
                    config.i2c_bus_number = int(bus_number)
                    break
                else:
                    print("\nPlease enter a valid selection")

            while True:
                debug_mode = input("""
Will you use OTA software in a simulation mode? [y/N]
Flashing itself is not possible in "sim" mode!\t\t\t\t""").lower()
                if not debug_mode:
                    debug_mode, config.debug_mode = False, False
                    print("defaulted to: no")
                    break
                elif debug_mode[0] == 'y':
                    debug_mode, config.debug_mode = True, True
                    break
                elif debug_mode[0] == 'n':
                    debug_mode, config.debug_mode = False, False
                    break
                else:
                    print("\nPlease enter a valid selection")

            if debug_mode:
                debug_user_name = input("\nWhat is your user name on sim/debug OS? \t\t\t\t")
                config.debug_user = debug_user_name
            else:
                config.debug_user = 'default'
            while True:
                old_hardware_mod = input("""
Are you using older, non-i2c hardware flashing mod? 
(nodes reset pins connected to gpio pins) [y/N]\t\t""").lower()
                if not old_hardware_mod:
                    old_hardware_mod, config.old_hw_mod = False, False
                    print("defaulted to: no")
                    break
                elif old_hardware_mod[0] == "y":
                    old_hardware_mod, config.old_hw_mod = True, True
                    break
                elif old_hardware_mod[0] == "n":
                    old_hardware_mod, config.old_hw_mod = False, False
                    break
                else:
                    print("\nPlease enter a valid selection")

            while old_hardware_mod:
                gpio_pins_assign = input("\nPins assignment? [default/custom/PCB | default: default]\t\t").lower()
                pins_valid_options = ['default', 'pcb', 'custom']
                if not gpio_pins_assign:
                    config.pins_assignment = 'default'
                    print("defaulted to: default")
                    break
                elif gpio_pins_assign not in pins_valid_options:
                    print("\nPlease enter a valid selection")
                    continue
                else:
                    config.pins_assignment = gpio_pins_assign
                    break
            else:
                config.pins_assignment = 'default'

            while True:
                user_is_beta_tester = input(
                    "\nAre you a beta tester for Install Manager? [y/N]\t\t").lower()
                if not user_is_beta_tester:
                    config.beta_tester = False
                    print("defaulted to: no")
                    break
                elif user_is_beta_tester in ['y', 'yes']:
                    config.beta_tester = True
                    break
                elif user_is_beta_tester in ['n', 'no']:
                    config.beta_tester = False
                    break
                else:
                    config.beta_tester = user_is_beta_tester
                    break

        if not advanced_wizard_flag:
            config.debug_mode = False
            config.debug_user = 'default'
            config.old_hw_mod = False
            config.pins_assignment = 'default'
            config.gpio_reset_pin = False
            config.i2c_bus_number = 1
            config.beta_tester = False

        print(f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}:

        User name:              {config.pi_user}
        RotorHazard version:    {config.rh_version}
        Country code:           {config.country}
        Nodes amount:           {config.nodes_number}
        Flashing port name:     {config.port_name}
        Old hardware mod:       {config.old_hw_mod}    
        Simulation mode:        {config.debug_mode}    
        Sim/Debug user name:    {config.debug_user}
        Pins assignment:        {config.pins_assignment}
        GPIO reset pin:         {config.gpio_reset_pin}
        I2C bus number:         {config.i2c_bus_number}
        Beta tester:            {config.beta_tester}
         
        Please check. Confirm? [yes/change/abort]\n""")
        valid_options = ['y', 'yes', 'n', 'no', "ch", 'change', 'abort']
        while True:
            selection = input().strip().lower()
            if selection in valid_options:
                break
            else:
                print("\nPlease enter a valid selection")
        if selection[0] == 'y':
            write_json(config, f"{home_dir}/RH_Install-Manager/updater-config.json")
            # Once we write out the json config we should re-load it just
            # to ensure consistency.
            config = load_config()
            print("Configuration saved.\n")
            sleep(1)
            conf_now_flag = 0
        if selection in ['ch', 'change', 'n', 'no']:
            conf_now_flag = 1
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            conf_now_flag = 0

        # Must return the new config from inside the if statements variable context.
        return conf_now_flag, config
    # Return the old config without change.
    return conf_now_flag, old_config


def conf_ota(config):
    """
        repeat the configuration script until
        the user either aborts, configures ota
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
