from time import sleep
import os
import json
from modules import clear_the_screen, Bcolors, logo_top, check_if_string_in_file
from nodes_flash import main as new_flashing
try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
except ModuleNotFoundError:
    print("GPIO import - failed")
    sleep(2)

"""
This is obsolete flashing protocol, left here only for some users.
New version is in i2c_nodes_flash.py file.
"""


def main():
    if os.path.exists("./updater-config.json"):
        with open('updater-config.json') as config_file:
            data = json.load(config_file)
    else:
        with open('distr-updater-config.json') as config_file:
            data = json.load(config_file)

    if os.path.exists("./updater-config.json"):
        if check_if_string_in_file('updater-config.json', 'assignment'):
            pins_assignment = data['pins_assignment']
        else:
            pins_assignment = 'default'
    else:
        pins_assignment = 'default'

    preferred_rh_version = data['RH_version']

    if preferred_rh_version == 'master':
        firmware_version = 'master'
    if preferred_rh_version == 'beta':
        firmware_version = 'beta'
    if preferred_rh_version == 'stable':
        firmware_version = 'stable'
    if preferred_rh_version == 'custom':
        firmware_version = 'stable'

    nodes_number = int(data['nodes_number'])

    # default to default pins. only update if they said so.
    reset_pins = [
        12  # node 1   # default 12
        , 16  # node 2   # default 16
        , 20  # node 3   # default 20
        , 21  # node 4   # default 21
        , 6  # node 5   # default 6
        , 13  # node 6   # default 13
        , 19  # node 7   # default 19
        , 26  # node 8   # default 26
    ]
    if pins_assignment == 'PCB' or pins_assignment == 'pcb':
        reset_pins = [
            12  # node 1   # default 12
            , 16  # node 2   # default 16
            , 4  # node 3   # default 4
            , 21  # node 4   # default 21
            , 6  # node 5   # default 6
            , 13  # node 6   # default 13
            , 19  # node 7   # default 19
            , 26  # node 8   # default 26
        ]
    if pins_assignment == 'custom':
        reset_pins = [
            0  # node 1   # custom pin assignment
            , 0  # node 2   # custom pin assignment
            , 0  # node 3   # custom pin assignment
            , 0  # node 4   # custom pin assignment
            , 0  # node 5   # custom pin assignment
            , 0  # node 6   # custom pin assignment
            , 0  # node 7   # custom pin assignment
            , 0  # node 8   # custom pin assignment
        ]

    if data['debug_mode']:
        linux_testing = True
    else:
        linux_testing = False

    if linux_testing:
        user = data['debug_user']
    else:
        user = data['pi_user']

    if not linux_testing:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(reset_pins[0], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[1], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[2], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[3], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[4], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[5], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[6], GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(reset_pins[7], GPIO.OUT, initial=GPIO.HIGH)

        def all_pins_high():
            GPIO.output(reset_pins[0], GPIO.HIGH)
            GPIO.output(reset_pins[1], GPIO.HIGH)
            GPIO.output(reset_pins[2], GPIO.HIGH)
            GPIO.output(reset_pins[3], GPIO.HIGH)
            GPIO.output(reset_pins[4], GPIO.HIGH)
            GPIO.output(reset_pins[5], GPIO.HIGH)
            GPIO.output(reset_pins[6], GPIO.HIGH)
            GPIO.output(reset_pins[7], GPIO.HIGH)
            sleep(0.05)

        def flash_a_node(reset_pin, user, firmware_version, firmware_number, node_number):
            all_pins_high()
            GPIO.output(reset_pin, GPIO.LOW)
            sleep(0.1)
            GPIO.output(reset_pin, GPIO.HIGH)
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                    flash:w:/home/{user}/RH-ota/firmware/obsolete/{firmware_version}/node_{firmware_number}.hex:i ")
            print(f"\n\t\t\t\t{Bcolors.BOLD}Node {node_number} - flashed{Bcolors.ENDC}\n\n")

    if linux_testing:
        def all_pins_high():
            print(f"\n\n\t\t\t/home/{user}/RH-ota/firmware/obsolete/{firmware_version}/X.hex")
            print("\n\t\t\t\t\t Linux - PC\n\n")
            sleep(0.3)

        def flash_a_node(reset_pin, user, firmware_version, firmware_number, node_number):
            print(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                    flash:w:/home/{user}/RH-ota/firmware/obsolete/{firmware_version}/node_{firmware_number}.hex:i ")
            print(f"\n\t\t\t\t{Bcolors.BOLD}Node {node_number} - flashed{Bcolors.ENDC}\n\n")

    def logo_update():
        print("""
        #######################################################################
        #                                                                     #
        #{bold}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s}#
        #                                                                     #
        #                          {bold}Thank you!{endc}                     #
        #                                                                     #
        #######################################################################\n\n
        """.format(nodes_number=nodes_number, bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE_S, endc=Bcolors.ENDC_S,
                   blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, orange=Bcolors.ORANGE_S, s=10 * ' '))

    def flash_all_nodes():
        for node in range(1, nodes_number + 1):
            pin = reset_pins[node - 1]
            flash_a_node(pin, user, firmware_version, node, node)

    def flash_all_gnd():
        for node in range(1, nodes_number + 1):
            pin = reset_pins[node - 1]
            flash_a_node(pin, user, firmware_version, 0, node)

    def flash_a_blink(reset_pin, user, firmware_version, node_number):
        all_pins_high()
        GPIO.output(reset_pin, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_pin, GPIO.HIGH)
        os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                flash:w:/home/{user}/RH-ota/firmware/obsolete/{firmware_version}/blink.hex:i ")
        print(f"\n\t\t\t\t{Bcolors.BOLD}Node {node_number} - flashed{Bcolors.ENDC}\n\n")
        sleep(1)

    def flash_all_blink():
        for node in range(1, nodes_number + 1):
            pin = reset_pins[node - 1]
            flash_a_blink(pin, user, firmware_version, node)

    def flash_each_node():
        def node_x_menu(sel_node):
            while True:
                print(f"""
                {Bcolors.BOLD}\n\t\t\tNode {str(sel_node)}  selected{Bcolors.ENDC}
                        Choose flashing type:\n{Bcolors.ENDC}
                1 - {Bcolors.GREEN}Node gets own dedicated firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}
                2 - Node ground-auto selection firmware
                3 - Flashes 'Blink' on the node
                4 - Abort
                {Bcolors.ENDC}""")
                selection = input()
                if selection == '1':
                    flash_a_node(reset_pins[sel_node - 1], user, firmware_version, sel_node, sel_node)
                    return
                if selection == '2':
                    flash_a_node(reset_pins[sel_node - 1], user, firmware_version, 0, sel_node)
                    return
                if selection == '3':
                    flash_a_blink(reset_pins[sel_node - 1], user, firmware_version, sel_node)
                    return
                if selection == '4':
                    break

        def node_menu():
            while True:
                clear_the_screen()
                logo_top(linux_testing)
                sleep(0.05)
                flash_node_menu = """
                                    {red}{bold}NODES MENU{endc}
                                {bold}
                        1 - Flash node 1        5 - Flash node 5
                    
                        2 - Flash node 2        6 - Flash node 6
                    
                        3 - Flash node 3        7 - Flash node 7
                    
                        4 - Flash node 4        8 - Flash node 8
                                {yellow}
                            'e'- Exit to main menu{endc}
                """.format(bold=Bcolors.BOLD, red=Bcolors.RED, yellow=Bcolors.YELLOW, endc=Bcolors.ENDC)
                print(flash_node_menu)
                selection = input("""
                        {bold}Which node do you want to program:{endc} """.format(bold=Bcolors.BOLD, endc=Bcolors.ENDC))
                if selection.isnumeric() and 1 <= int(selection) <= 8:
                    node_x_menu(int(selection))
                elif selection == 'e':
                    break

        node_menu()

    def gpio_state():
        clear_the_screen()
        logo_top(linux_testing)
        print("\n\n\n")
        os.system(f"echo {reset_pins[0]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[1]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[2]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[3]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[4]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[5]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[6]} > /sys/class/GPIO/unexport")
        os.system(f"echo {reset_pins[7]} > /sys/class/GPIO/unexport")
        os.system("echo 19 > /sys/class/GPIO/unexport")
        os.system("echo 20 > /sys/class/GPIO/unexport")
        os.system("echo 21 > /sys/class/GPIO/unexport")
        print("\n\n        DONE\n\n")
        sleep(0.3)

    def nodes_update():
        while True:
            clear_the_screen()
            logo_top(linux_testing)
            sleep(0.05)
            node_menu = """\n
                            {bold}{underline}CHOOSE FLASHING TYPE:{endc}
            
                    {green}{bold}1 - Every Node gets own dedicated firmware - rec.{endc}
                    
                    {bold}2 - Nodes using ground-auto numbering firmware
                    
                    3 - Flash 'Blink' on every node
                    
                    4 - Flash each node individually
                    
                    5 - Fix GPIO pins state - obsolete
                    
                    6 - Enter new (I2C) flashing menu
                    
                    {yellow}e - Exit to main menu{endc}
            """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                       endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
            print(node_menu)
            sleep(0.1)
            selection = input()
            if selection == '1':
                flash_all_nodes()
                logo_update()
                sleep(3)
            if selection == '2':
                flash_all_gnd()
                logo_update()
                sleep(3)
            if selection == '3':
                flash_all_blink()
                logo_update()
                sleep(3)
            if selection == '4':
                flash_each_node()
            if selection == '5':
                gpio_state()
            if selection == '6':
                new_flashing()
            if selection == 'e':
                break

    nodes_update()


if __name__ == '__main__':
    main()
