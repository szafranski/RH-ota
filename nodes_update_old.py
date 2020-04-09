from time import sleep
import os
from modules import clear_the_screen, Bcolors, logo_top, load_config
from nodes_flash import main as new_flashing

try:
    # GPIO is only definable on the pi.
    # Try and import it but continue if it is not found.
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
except ModuleNotFoundError:
    print("GPIO import - failed - works only on Pi")
    print("Try manually install RPI.GPIO with 'pip3 install rpi.gpio'")
    sleep(1)


"""
This is obsolete flashing protocol, left here only for first users in mind.
New version is in i2c_nodes_flash.py file. 
"""


def pins_assignment(config):

    # default to default pins. only update if they said so.
    reset_pins = [
        12,  # node 1   # default 12
        16,  # node 2   # default 16
        20,  # node 3   # default 20
        21,  # node 4   # default 21
        6,  # node 5   # default 6
        13,  # node 6   # default 13
        19,  # node 7   # default 19
        26  # node 8   # default 26
    ]
    if config.pins_assignment.lower() == 'pcb':
        reset_pins = [
            12,  # node 1   # default 12
            16,  # node 2   # default 16
            4,  # node 3   # default 4
            21,  # node 4   # default 21
            6,  # node 5   # default 6
            13,  # node 6   # default 13
            19,  # node 7   # default 19
            26  # node 8   # default 26
        ]
    if pins_assignment == 'custom':
        reset_pins = [
            0,  # node 1   # custom pin assignment
            0,  # node 2   # custom pin assignment
            0,  # node 3   # custom pin assignment
            0,  # node 4   # custom pin assignment
            0,  # node 5   # custom pin assignment
            0,  # node 6   # custom pin assignment
            0,  # node 7   # custom pin assignment
            0  # node 8   # custom pin assignment
        ]

    return reset_pins


def gpio_init(config, reset_pins):
    if not config.debug_mode:
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


def all_pins_high(config, reset_pins):
    if not config.debug_mode:
        GPIO.output(reset_pins[0], GPIO.HIGH)
        GPIO.output(reset_pins[1], GPIO.HIGH)
        GPIO.output(reset_pins[2], GPIO.HIGH)
        GPIO.output(reset_pins[3], GPIO.HIGH)
        GPIO.output(reset_pins[4], GPIO.HIGH)
        GPIO.output(reset_pins[5], GPIO.HIGH)
        GPIO.output(reset_pins[6], GPIO.HIGH)
        GPIO.output(reset_pins[7], GPIO.HIGH)
        sleep(0.05)
    else:
        print(f"\n\n\t\t\t/home/{config.user}/RH-ota/firmware/obsolete/{config.rh_version}/X.hex")
        print("\n\t\t\t\t\t Linux - PC\n\n")
        sleep(0.3)


def logo_update(config):
    print("""
    #######################################################################
    #                                                                     #
    #{bold}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s}#
    #                                                                     #
    #                          {bold}Thank you!{endc}                     #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=config.nodes_number, bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE_S,
               endc=Bcolors.ENDC_S, blue=Bcolors.BLUE, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S,
               orange=Bcolors.ORANGE_S, s=10 * ' '))


def flash_a_node(config, reset_pin, node_number):
    if not config.debug_mode:
        all_pins_high(config, pins_assignment(config))
        GPIO.output(reset_pin, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_pin, GPIO.HIGH)
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                flash:w:/home/{config.user}/RH-ota/firmware/{config.rh_version}/node_0.hex:i ")
    if config.debug_mode:
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                flash:w:/home/{config.user}/RH-ota/firmware/{config.rh_version}/node_0.hex:i ")
    print(f"\n\t\t\t\t{Bcolors.BOLD}Node {node_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue.\n")


def flash_a_blink(config, reset_pin, node_number):
    if not config.debug_mode:
        all_pins_high(config, pins_assignment(config))
        GPIO.output(reset_pin, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_pin, GPIO.HIGH)
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
    if config.debug_mode:
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
    print(f"\n\t\t\t\t{Bcolors.BOLD}Node {node_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue.\n")


def flash_all_blink(config, reset_pins):
    for node in range(1, config.nodes_number + 1):
        pin = reset_pins[node - 1]
        flash_a_blink(config, pin, node)


def flash_all_gnd(config, reset_pins):
    for node in range(1, config.nodes_number + 1):
        pin = reset_pins[node - 1]
        flash_a_node(config, pin, node)


def flash_each_node(config):
    def specific_node_menu(sel_node):
        while True:
            print(f"""
            {Bcolors.BOLD}\n\t\t\tNode {str(sel_node)}  selected{Bcolors.ENDC}
                    Choose flashing type:{Bcolors.ENDC}

            1 - {Bcolors.GREEN}Flash firmware on the node{Bcolors.ENDC}{Bcolors.BOLD}

            2 - Flash 'blink' on the node

            a - Abort
            {Bcolors.ENDC}""")
            selection = input()
            if selection == '1':
                flash_a_node(config, pins_assignment(config)[sel_node - 1], sel_node)
                return
            if selection == '2':
                flash_a_blink(config, pins_assignment(config)[sel_node - 1], sel_node)
                return
            if selection == 'a':
                break

    def node_menu():
        while True:
            clear_the_screen()
            logo_top(config.debug_mode)
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
                specific_node_menu(int(selection))
            elif selection == 'e':
                break

    node_menu()


def gpio_state(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    print("\n\n\n")
    os.system(f"echo {pins_assignment(config)[0]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[1]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[2]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[3]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[4]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[5]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[6]} > /sys/class/GPIO/unexport")
    os.system(f"echo {pins_assignment(config)[7]} > /sys/class/GPIO/unexport")
    os.system("echo 19 > /sys/class/GPIO/unexport")
    os.system("echo 20 > /sys/class/GPIO/unexport")
    os.system("echo 21 > /sys/class/GPIO/unexport")
    print("\n\n\t\tDONE\n\n")
    sleep(0.3)


def nodes_update(config):
    gpio_init(config, pins_assignment(config))
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        node_menu = """\n
                        {bold}{underline}CHOOSE FLASHING TYPE:{endc}
        
                {green}{bold}1 - Nodes using ground-auto numbering firmware - rec.{endc}
                
                2 - Flash 'blink' on every node
                
                3 - Flash each node individually
                
                4 - Fix GPIO pins state - obsolete
                
                5 - Enter new (I2C) flashing menu
                
                {yellow}e - Exit to main menu{endc}
        """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                   endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
        print(node_menu)
        sleep(0.1)
        selection = input()
        if selection == '1':
            flash_all_gnd(config, pins_assignment(config))
            logo_update(config)
            sleep(3)
        if selection == '2':
            flash_all_blink(config, pins_assignment(config))
            logo_update(config)
            sleep(3)
        if selection == '3':
            flash_each_node(config)
        if selection == '4':
            gpio_state(config)
        if selection == '5':
            new_flashing()
        if selection == 'e':
            break


def main():
    config = load_config()
    nodes_update(config)


if __name__ == '__main__':
    main()
