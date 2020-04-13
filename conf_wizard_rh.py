from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top, write_json
from pathlib import Path


def conf_check():
    conf_now_flag = 0
    if os.path.exists(f"./../RotorHazard/src/server/config.json"):
        print("\n\tLooks that you have Rotorhazard software already configured.")
        valid_options_conf_check = ['y', 'yes', 'n', 'no']
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [yes/no]\t\t").strip()
            if cont_conf in valid_options_conf_check:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if cont_conf[0] == 'y':
            conf_now_flag = 1
        elif cont_conf[0] == 'n':
            conf_now_flag = 0
    else:
        conf_now_flag = 1
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
If you want to use value given as default, just hit 'Enter'.\n""")
        rh_config["GENERAL"] = {}
        admin_name = input("\nWhat will be admin user name on RotorHazard page? [default: admin]\t")
        admin_name = 'admin' if len(admin_name) == 0 else None
        rh_config["GENERAL"]["ADMIN_USERNAME"] = admin_name
        admin_pass = input("\nWhat will be admin password on RotorHazard page? [default: rotorhazard]\t")
        admin_pass = 'rotorhazard' if len(admin_pass) == 0 else None
        rh_config["GENERAL"]["ADMIN_PASSWORD"] = admin_pass
        while True:
            port = input("\nWhich port will you use with RotorHazard? [default: 5000]\t\t")
            if len(port) == 0:
                port = 5000
            elif not port.isdigit() or int(port) < 0:
                print("\nPlease enter correct value!")
                continue
            rh_config['GENERAL']['HTTP_PORT'] = int(port)
            break
        rh_config["SENSORS"] = {}
        rh_config["LED"] = {}
        print("\nAre you planning to use LEDs in your system? [y/n]\n")
        valid_options = ['y', 'n']
        led_present_flag = False
        while True:
            selection = input("\t")
            if selection in valid_options:
                if selection == 'y':
                    led_present_flag = True
                if selection == 'n':
                    led_present_flag = False
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if led_present_flag:
            while True:
                led_count = input("\nHow many LEDs will you use in your system?\t\t\t\t")
                if not led_count.isdigit() or int(led_count) < 0:
                    print("\nPlease enter correct value!")
                else:
                    rh_config["LED"]['LED_COUNT'] = int(led_count)
                    break
            while True:
                led_pin_nr = input("\nWhich GPIO pin is connected to your LEDs data pin? [default: 18]\t")
                led_pins_allowed = [10, 12, 13, 18, 19, 21, 31, 38, 40, 41, 45, 52, 53]
                if len(led_pin_nr) == 0:
                    led_pin_nr = 18
                elif led_pin_nr not in str(led_pins_allowed):
                    print("\nPlease enter correct value!")
                    continue
                rh_config["LED"]['LED_PIN'] = int(led_pin_nr)
                break
            while True:
                led_inv = input("\nIs LED data pin output inverted? [y/N | default: no]\t\t\t")
                led_inv_allowed_values = ['y', 'n', 'Y', 'N']
                if len(led_inv) == 0:
                    led_inv = False
                elif led_inv not in led_inv_allowed_values:
                    print("\nPlease enter correct value!")
                    continue
                rh_config["LED"]['LED_INVERT'] = led_inv
                break
            while True:
                led_channel = input("\nWhat channel (not pin!) will be used with your LEDs? [default: 0]\t")
                if len(led_channel) == 0:
                    led_channel = 0
                elif not led_channel.isdigit() or int(led_channel) < 0 or int(led_channel) > 1:
                    print("\nPlease enter correct value!")
                    continue
                rh_config["LED"]['LED_CHANNEL'] = int(led_channel)
                break
            while True:
                panel_rot = input("\nBy how many degrees is your panel rotated? [0/90/180/270 | default: 0]\t")
                panel_rot_values_allowed = ['0', '90', '180', '270']
                if len(panel_rot) == 0:
                    panel_val = 0
                elif panel_rot not in panel_rot_values_allowed:
                    print("\nPlease enter correct value!")
                    continue
                else:
                    panel_val = (int(panel_rot) / 90)
                rh_config["LED"]['PANEL_ROTATE'] = int(panel_val)
                break
            while True:
                inv_rows = input("\nAre your panel rows inverted? [y/N | default: no]\t\t\t")
                inv_rows_allowed_values = ['y', 'Y', 'n', 'N']
                if inv_rows not in inv_rows_allowed_values:
                    print("\nPlease enter correct value!")
                    continue
                inv_rows_val = True if inv_rows.lower() is 'y' else False
                rh_config["LED"]['INVERTED_PANEL_ROWS'] = inv_rows_val
                break

        if not led_present_flag:
            rh_config["LED"]['LED_COUNT'] = 0
            rh_config["LED"]['LED_PIN'] = 10
            rh_config["LED"]['LED_INVERT'] = False
            rh_config["LED"]['LED_CHANNEL'] = 0
            rh_config["LED"]['PANEL_ROTATE'] = 0
            rh_config["LED"]['INVERTED_PANEL_ROWS'] = False
            print("\nLED configuration set to default values.\n\n")
            sleep(1.2)

        print("\nDo you want to enter advanced wizard? [y/N]\n")
        valid_options = ['y', 'Y', 'n', 'N']
        while True:
            selection = input("\t").strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
                continue
        adv_wiz_flag = True if selection.lower() is 'y' else False

        if adv_wiz_flag:
            while True:
                led_dma = input("\nLED DMA you will use in your system? [default: 10]\t\t\t")
                if len(led_dma) == 0:
                    led_dma = 10
                elif not led_dma.isdigit() or int(led_dma) < 0:
                    print("\nPlease enter correct value!")
                    continue
                rh_config["LED"]['LED_DMA'] = int(led_dma)
                break
            while True:
                led_freq = input("\nWhat LED frequency will you use? [default: 800000]\t\t\t")
                if len(led_freq) == 0:
                    led_freq = 800000
                if (led_freq.isalpha() or int(led_freq) < 0 or int(led_freq) > 800000) and led_freq != 'def':
                    print("\nPlease enter correct value!")
                    continue
                rh_config["LED"]['LED_FREQ_HZ'] = led_freq
                break

            while True:
                debug_mode = input("\nWill you use RotorHazard in debug mode? [y/N | default: no]\t\t")
                debug_mode_allowed_values = ['y', 'n', 'Y', 'N']
                if debug_mode not in debug_mode_allowed_values:
                    print("\nPlease enter correct value!")
                    continue
                debug = True if debug_mode.lower() is 'y' else False
                rh_config['GENERAL']['DEBUG'] = debug
                break

            while True:
                cors = input("\nCORS hosts allowed? [default: all]\t\t\t\t\t")
                if cors in ['*', 'all'] or len(cors) == 0:
                    rh_config['GENERAL']['CORS_ALLOWED_HOSTS'] = "*"
                    break
                elif len(cors) > 3:
                    rh_config['GENERAL']['CORS_ALLOWED_HOSTS'] = cors
                    break
                else:
                    print("\nPlease enter correct value!")

            while True:
                serial_ports = input("\nWhich USB ports you will use? [default: 'none']\t\t\t\t").strip()
                if serial_ports in ['none', '0', 'n', 'N'] or len(serial_ports) == 0:
                    rh_config['SERIAL_PORTS'] = []
                    break
                else:
                    rh_config['SERIAL_PORTS'] = [f"{serial_ports}"]
                    break
        if not adv_wiz_flag:
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
        if selection == 'y' or selection == 'yes':
            write_json(rh_config, f"{home_dir}/RotorHazard/src/server/config.json")
            print("Configuration saved.\n")
            sleep(0.5)
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
