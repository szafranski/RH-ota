from time import sleep
import os
import json
from modules import clear_the_screen, Bcolors, logo_top, load_config

home_dir = os.path.expanduser('~')

clear_the_screen()
parser, config = load_config()
logo_top(config.debug_user)

if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']

conf_now_flag = '0'

admin_name = 0
admin_pass = 0
port = 0
led_count = 0
led_pin = 0
led_inv = 0
led_channel = 0
panel_rot = 0
inv_rows = 0
dma = 0
freq = 0
debug = 0
cores_val = 0
serial_ports = 0
led_inv_val = 0
inv_rows_val = 0
adv_wiz_flag = 0
led_present_flag = 0

# todo David - if above have sense?

configuration_content = {
    "GENERAL": {
        "HTTP_PORT": {port},
        "ADMIN_USERNAME": {admin_name},
        "ADMIN_PASSWORD": {admin_pass},
        "DEBUG": {debug},
        "CORS_ALLOWED_HOSTS": {cores_val}
    },
    "SENSORS": {
    },
    "SERIAL_PORTS": [{serial_ports}],
    "LED": {
        "LED_COUNT": {led_count},
        "LED_PIN": {led_pin},
        "LED_FREQ_HZ": {freq},
        "LED_DMA": {dma},
        "LED_INVERT": {led_inv},
        "LED_CHANNEL": {led_channel},
        "PANEL_ROTATE": {panel_rot},
        "INVERTED_PANEL_ROWS": {led_inv}
    }
}


def conf_check():
    global conf_now_flag
    if os.path.exists(f"/home/{user}/RotorHazard/src/server/config.json"):
        print("\n\tLooks that you already have RotorHazard server configured.")
        valid_options_conf_check = ['y', 'yes', 'n', 'no']
        while True:
            cont_conf = input("\n\tOverwrite and continue anyway? [yes/no]\t\t").strip()
            if cont_conf in valid_options_conf_check:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if cont_conf == 'y' or cont_conf == 'yes':
            conf_now_flag = 1
            pass
        if cont_conf == 'n' or cont_conf == 'no':
            conf_now_flag = 0
    else:
        conf_now_flag = 1


conf_check()

if conf_now_flag:
    while True:
        print("""\n
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.\n""")
        os.system(f"rm /home/{user}/.wizarded-rh-config.json >/dev/null 2>&1")
        os.system(f"cp /home/{user}/RotorHazard/src/server/config-dist.json /home/"
                  f"{user}/RH-ota/.wizarded-rh-config.json")
        admin_name = input("\nWhat will be admin user name on RotorHazard page? [default: admin]\t")
        admin_pass = input("\nWhat will be admin password on RotorHazard page? [default: rotorhazard]\t")
        while True:
            port = input("\nWhich port will you use with RotorHazard? [default: 5000]\t\t")
            if not port.isdigit() or int(port) < 0:
                print("\nPlease enter correct value!")
            else:
                break
        print("\nAre you planning to use LEDs in your system? [yes/no]\n")
        valid_options = ['y', 'yes', 'n', 'no']
        while True:
            selection = input("\t")
            if selection in valid_options:
                if selection == 'y' or selection == 'yes':
                    led_present_flag = True
                if selection == 'n' or selection == 'no':
                    led_present_flag = False
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if led_present_flag:
            while True:
                led_count = input("\nHow many LEDs will you use in your system? [default: 0]\t\t\t")
                if not led_count.isdigit() or int(led_count) < 0:
                    print("\nPlease enter correct value!")
                else:
                    break
            while True:
                led_pin = input("\nWhich GPIO pin is connected to your LEDs data pin? [default: 10]\t")
                if not led_pin.isdigit() or int(led_pin) < 0 or int(led_pin) > 40:
                    print("\nPlease enter correct value!")
                else:
                    break
            while True:
                led_inv = input("\nIs LED data pin output inverted? [yes/no | default: no]\t\t\t")
                led_inv_allowed_values = ['yes', 'no', 'false', 'true', 'y', 'n']
                if led_inv not in led_inv_allowed_values:
                    print("\nPlease enter correct value!")
                else:
                    if led_inv in ['yes', '1', 'y']:
                        led_inv_val = 'true'
                    elif led_inv in ['no', '0', 'n']:
                        led_inv_val = 'false'
                    break
            while True:
                led_channel = input("\nWhat channel (not pin!) will be used with your LEDs? [default: 0]\t")
                if not led_channel.isdigit() or int(led_channel) < 0 or int(led_channel) > 1:
                    print("\nPlease enter correct value!")
                else:
                    break
            while True:
                panel_rot = input("\nBy how many degrees is your panel rotated? [0/90/180/270 | default: 0]\t")
                panel_rot_values_allowed = ['0', '90', '180', '270']
                if panel_rot not in panel_rot_values_allowed:
                    print("\nPlease enter correct value!")
                else:
                    panel_val = (int(panel_rot) / 90)
                    break
            while True:
                inv_rows = input("\nAre your panel rows inverted? [yes/no | default: no]\t\t\t")
                inv_rows_allowed_values = ['yes', 'no', 'false', 'true', 'y', 'n']
                if inv_rows not in inv_rows_allowed_values:
                    print("\nPlease enter correct value!")
                else:
                    if inv_rows in ['yes', '1', 'y']:
                        inv_rows_val = 'true'
                    elif inv_rows in ['no', '0', 'n']:
                        inv_rows_val = 'false'
                    break

        if not led_present_flag:
            led_count = '0'
            led_pin = '10'
            led_inv = 'false'
            led_channel = '0'
            panel_rot = '0'
            inv_rows = 'false'
            print("\nLED configuration set to default values.\n\n")
            sleep(1.2)

        print("\nDo you want to enter advanced wizard? [yes/no]\n")
        valid_options = ['y', 'yes', 'n', 'no']
        while True:
            selection = input("\t").strip()
            if selection in valid_options:
                break
            else:
                print("\ntoo big fingers :( wrong command. try again! :)")
        if selection == 'y' or selection == 'yes':
            adv_wiz_flag = True
        if selection == 'n' or selection == 'no':
            adv_wiz_flag = False

        if adv_wiz_flag:
            while True:
                dma = input("\nLED DMA you will use in your system? [default: 10]\t\t\t")
                if not dma.isdigit() or int(dma) < 0:
                    print("\nPlease enter correct value!")
                else:
                    break
            while True:
                freq = input("\nWhat LED frequency will you use? [default: 800000 - you can type 'def']\t")
                if (freq.isalpha() or int(freq) < 0 or int(freq) > 800000) and freq != 'def':
                    print("\nPlease enter correct value!")
                elif freq == 'def':
                    break
                else:
                    break
            while True:
                debug_mode = input("\nWill you use RotorHazard in debug mode? [yes/no | default: no]\t\t")
                debug_mode_allowed_values = ['yes', 'no', '1', '0', 'y', 'n']
                if debug_mode not in debug_mode_allowed_values:
                    print("\nPlease enter correct value!")
                else:
                    debug = 'false'
                    if debug_mode in ['yes', '1', 'y']:
                        debug = 'true'
                    elif debug_mode in ['no', '0', 'n']:
                        debug = 'false'
                    break
            while True:
                cores = input("\nHome many cores will be available for hosts? [1/2/3/all | default: all]\t")
                cores_values_allowed = ['1', '2', '3', '4', 'all', '*']
                if cores not in cores_values_allowed:
                    print("\nPlease enter correct value!")
                else:
                    if cores in ['1', '2', '3']:
                        cores_val = str(cores)
                    elif cores == 'all':
                        cores_val = 'all'
                    else:
                        cores_val = '*'
                    break
            while True:
                serial_ports = input("\nWhich serial ports will you use? [default: 'none']\t\t\t").strip()
                if serial_ports in ['none', '0', 'no']:
                    break
                else:
                    break
        if not adv_wiz_flag:
            debug = 'no'
            cores_val = 'all'
            serial_ports = 'none'
            dma = '10'
            freq = '800000'
            print("\nAdvanced configuration set to default values.\n\n")
            sleep(1.2)
        rh_configuration_summary = f"""\n\n
            {Bcolors.UNDERLINE}CONFIGURATION{Bcolors.ENDC}

        Admin name:         {admin_name}
        Admin password:     {admin_pass}
        RotorHazard port:   {port}
        LED amount:         {led_count}
        LED pin:            {led_pin}
        LED inverted:       {led_inv}
        LED channel:        {led_channel}
        LED panel rotate:   {panel_rot}
        LED rows inverted:  {inv_rows}
        LED DMA:            {dma}
        LED frequency:      {freq}
        Debug mode:         {debug}
        Cores allowed:      {cores_val}
        Serial ports:       {serial_ports}

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
            with open(f'/home/{user}/Pulpit/test', 'w') as json_cfg:
                json.dump(configuration_content, json_cfg)
            print("Configuration saved.\n")
            sleep(0.5)
            break
        if selection in ['change', 'n', 'no']:
            continue
        if selection == 'abort':
            print("Configuration aborted.\n")
            sleep(0.5)
            break
else:
    os.system("exit")
