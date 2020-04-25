from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top, write_json
from pathlib import Path


def conf_check():
    conf_now_flag = 1
    if os.path.exists(f"./../RotorHazard/src/server/config.json"):
        print("\n\tLooks that you have Rotorhazard software already configured.")
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [y/n]\t\t").lower()
            if not cont_conf:
                print("answer defaulted to: yes")
                break
            elif cont_conf[0] == 'y':
                conf_now_flag = True
                break
            elif cont_conf[0] == 'n':
                conf_now_flag = False
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")

    return conf_now_flag


def do_config():
    home_dir = str(Path.home())
    clear_the_screen()
    logo_top(False)

    conf_now_flag = conf_check()

    if conf_now_flag:
        rh_config = {}
        print("""\n
Please type your configuration data. It can be modified later.
If you want to use value given as default, just hit 'Enter'.
""")
        rh_config["GENERAL"] = {}
        admin_name = input("\nWhat will be admin user name on RotorHazard page? [default: admin]\t")
        if not admin_name:
            admin_name = 'admin'
            print("defaulted to: 'admin'")
        rh_config["GENERAL"]["ADMIN_USERNAME"] = admin_name
        admin_pswd = input("\nWhat will be admin password on RotorHazard page? [default: rotorhazard]\t")
        if not admin_pswd:
            admin_pswd = 'rotorhazard'
            print("defaulted to: 'rotorhazard'")
        rh_config["GENERAL"]["ADMIN_PASSWORD"] = admin_pswd
        while True:
            led_port_nr = input("\nWhich port will you use with RotorHazard? [default: 5000]\t\t")
            if not led_port_nr:
                led_port_nr = 5000
                print("defaulted to: 5000")
                break
            elif led_port_nr.isdigit():
                break
            elif not led_port_nr.isdigit():
                print("\nPlease enter correct value!")
        rh_config['GENERAL']['HTTP_PORT'] = int(led_port_nr)
        rh_config["SENSORS"] = {}
        rh_config["LED"] = {}

        while True:
            print("\nAre you planning to use LEDs in your system? [y/n]\n")
            selection = input("\t").lower()
            if selection[0] == 'y':
                led_present_flag = True
                break
            elif selection[0] == 'n':
                led_present_flag = False
                break
            else:
                print("\nPlease enter correct value!")

        if led_present_flag:
            while True:
                led_amount = input("\nHow many LEDs will you use in your system?\t\t\t\t")
                if led_amount.isdigit():
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_COUNT'] = int(led_amount)

            while True:
                led_data_pin_nr = input("\nWhich GPIO pin is connected to your LEDs data pin? [default: 18]\t")
                led_pins_allowed = ['10', '12', '13', '18', '19', '21', '31', '38', '40', '41', '45', '52', '53']
                if not led_data_pin_nr:
                    led_data_pin_nr = 18
                    print("defaulted to: 18")
                    break
                elif led_data_pin_nr in led_pins_allowed:
                    led_data_pin_nr = int(led_data_pin_nr)
                    break
                elif led_data_pin_nr.isdigit() and led_data_pin_nr not in led_pins_allowed:
                    print("That pin cannot be used for that purpose")
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_PIN'] = int(led_data_pin_nr)

            while True:
                led_output_inverted = input("\nIs LED data pin output inverted? [y/N | default: no]\t\t\t").lower()
                if not led_output_inverted:
                    led_output_inverted = False
                    print("defaulted to: no")
                    break
                elif led_output_inverted[0] == 'y':
                    led_output_inverted = True
                    break
                elif led_output_inverted[0] == 'n':
                    led_output_inverted = False
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_INVERT'] = led_output_inverted

            while True:
                led_channel_nr = input("\nWhat channel (not pin!) will be used with your LEDs? [default: 0]\t")
                if not led_channel_nr:
                    led_channel_nr = 0
                    print("defaulted to: 0")
                    break
                elif led_channel_nr.isdigit():
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_CHANNEL'] = int(led_channel_nr)

            while True:
                led_panel_rotation = input("\nBy how many degrees is your panel rotated? [0/90/180/270 | default: 0]\t")
                panel_rot_values_allowed = ['0', '90', '180', '270']
                if not led_panel_rotation:
                    led_panel_rotation = 0
                    print("defaulted to: 0")
                    break
                elif led_panel_rotation in panel_rot_values_allowed:
                    led_panel_rotation = (int(led_panel_rotation) / 90)
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['PANEL_ROTATE'] = int(led_panel_rotation)

            while True:
                led_rows_inverted = input("\nAre your panel rows inverted? [y/N | default: no]\t\t\t").lower()
                if not led_rows_inverted:
                    led_rows_inverted = False
                    print("defaulted to: no")
                    break
                elif led_rows_inverted[0] == 'y':
                    led_rows_inverted = True
                    break
                elif led_rows_inverted[0] == 'n':
                    led_rows_inverted = False
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['INVERTED_PANEL_ROWS'] = led_rows_inverted

        if not led_present_flag:
            rh_config["LED"]['LED_COUNT'] = 0
            rh_config["LED"]['LED_PIN'] = 10
            rh_config["LED"]['LED_INVERT'] = False
            rh_config["LED"]['LED_CHANNEL'] = 0
            rh_config["LED"]['PANEL_ROTATE'] = 0
            rh_config["LED"]['INVERTED_PANEL_ROWS'] = False
            print("\nLED configuration set to default values.\n\n")
            sleep(1.2)

        print("\nDo you want to enter advanced wizard? [y/N | default: no]\n")
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
                print("\ntoo big fingers :( wrong command. try again! :)")

        if advanced_wizard_flag:
            while True:
                led_dma_nr = input("\nLED DMA you will use in your system? [default: 10]\t\t\t")
                if not led_dma_nr:
                    led_dma_nr = 10
                    print("defaulted to: 10")
                    break
                elif led_dma_nr.isdigit():
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_DMA'] = int(led_dma_nr)

            while True:
                led_frequency = input("\nWhat LED frequency will you use? [default: 800000]\t\t\t")
                if not led_frequency:
                    led_frequency = 800000
                    print("defaulted to: 800000")
                    break
                elif led_frequency.isdigit() and int(led_frequency) < 800000:
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config["LED"]['LED_FREQ_HZ'] = int(led_frequency)

            while True:
                debug_mode = input("\nWill you use RotorHazard in debug mode? [y/N | default: no]\t\t").lower()
                if not debug_mode:
                    debug_mode = False
                    print("defaulted to: no")
                    break
                elif debug_mode[0] == 'y':
                    debug_mode = True
                    break
                elif debug_mode[0] == 'n':
                    debug_mode = False
                    break
                else:
                    print("\nPlease enter correct value!")
            rh_config['GENERAL']['DEBUG'] = debug_mode

            cors = input("\nCORS hosts allowed? [default: all]\t\t\t\t\t")
            if not cors:
                cors = "*"
                print("defaulted to: all")
            elif cors in ['*', 'all']:
                cors = "*"
            rh_config['GENERAL']['CORS_ALLOWED_HOSTS'] = cors

            while True:
                serial_ports = input("\nWhich USB ports you will use? [default: 'none']\t\t\t\t").strip().lower()
                if not serial_ports:
                    serial_ports = []
                    print("defaulted to: none")
                    break
                elif serial_ports in ['none', 'n', 'N']:
                    serial_ports = []
                    break
                else:
                    serial_ports = [f"{serial_ports}"]
                    break
            rh_config['SERIAL_PORTS'] = serial_ports

        if not advanced_wizard_flag:
            rh_config['GENERAL']['DEBUG'] = False
            rh_config['GENERAL']['CORS_ALLOWED_HOSTS'] = '*'
            rh_config['SERIAL_PORTS'] = []
            rh_config['LED']['LED_DMA'] = 10
            rh_config['LED']['LED_FREQ_HZ'] = 800000
            print("\nAdvanced configuration set to default values.\n\n")
            sleep(1.2)

        rh_configuration_summary = f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}

        Admin name:         {rh_config["GENERAL"]["ADMIN_USERNAME"]}
        Admin password:     {rh_config["GENERAL"]["ADMIN_PASSWORD"]}
        RotorHazard port:   {rh_config["GENERAL"]["HTTP_PORT"]}
        LED amount:         {rh_config["LED"]['LED_COUNT']}
        LED pin:            {rh_config["LED"]['LED_PIN']}
        LED inverted:       {rh_config["LED"]['LED_INVERT']}
        LED channel:        {rh_config["LED"]['LED_CHANNEL']}
        LED panel rotate:   {rh_config["LED"]['PANEL_ROTATE']}
        LED rows inverted:  {rh_config["LED"]['INVERTED_PANEL_ROWS']}
        LED DMA:            {rh_config['LED']['LED_DMA']}
        LED frequency:      {rh_config['LED']['LED_FREQ_HZ']}
        Debug mode:         {rh_config['GENERAL']['DEBUG']}
        CORS allowed:       {rh_config['GENERAL']['CORS_ALLOWED_HOSTS']}
        Serial ports:       {rh_config['SERIAL_PORTS']}

        Please check. Confirm? [yes/change/abort]\n"""
        print(rh_configuration_summary)
        valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
        while True:
            selection = input().strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if selection[0] == 'y':
            write_json(rh_config, f"{home_dir}/RotorHazard/src/server/config.json")
            print("Configuration saved.\n")
            sleep(1)
            conf_now_flag = 0
        if selection in ['change', 'n', 'no']:
            conf_now_flag = 1
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            conf_now_flag = 0

    return conf_now_flag


def conf_rh():
    """
        repeat the configuration script until
        the user ether aborts, configures ota
        or it was already configured.
    :return:
    """
    config_now = 1
    while config_now:
        config_now = do_config()


def main():
    conf_rh()


if __name__ == "__main__":
    main()
