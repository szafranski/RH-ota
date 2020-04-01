from time import sleep
import os
import json
from modules import clear_the_screen, Bcolors, logo_top, check_if_string_in_file, load_config

if os.path.exists("../updater-config.json"):
    with open('../updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('../distr-updater-config.json') as config_file:
        data = json.load(config_file)

if os.path.exists("./updater-config.json"):
    if check_if_string_in_file('updater-config.json', 'assignment'):
        pins_assignment = data['pins_assignment']
    else:
        pins_assignment = 'default'
else:
    pins_assignment = 'default'

preferred_RH_version = data['RH_version']

if preferred_RH_version == 'master':
    firmware_version = 'master'
if preferred_RH_version == 'beta':
    firmware_version = 'beta'
if preferred_RH_version == 'stable':
    firmware_version = 'stable'
if preferred_RH_version == 'custom':
    firmware_version = 'stable'

nodes_number = data['nodes_number']

if pins_assignment == 'PCB' or pins_assignment == 'pcb':
    reset_1 = 12  # node 1   # default 12
    reset_2 = 16  # node 2   # default 16
    reset_3 = 4  # node 3   # default 4
    reset_4 = 21  # node 4   # default 21
    reset_5 = 6  # node 5   # default 6
    reset_6 = 13  # node 6   # default 13
    reset_7 = 19  # node 7   # default 19
    reset_8 = 26  # node 8   # default 26
if pins_assignment == 'default':
    reset_1 = 12  # node 1   # default 12
    reset_2 = 16  # node 2   # default 16
    reset_3 = 20  # node 3   # default 20
    reset_4 = 21  # node 4   # default 21
    reset_5 = 6  # node 5   # default 6
    reset_6 = 13  # node 6   # default 13
    reset_7 = 19  # node 7   # default 19
    reset_8 = 26  # node 8   # default 26
if pins_assignment == 'custom':
    reset_1 = 0  # node 1   # custom pin assignment
    reset_2 = 0  # node 2   # custom pin assignment
    reset_3 = 0  # node 3   # custom pin assignment
    reset_4 = 0  # node 4   # custom pin assignment
    reset_5 = 0  # node 5   # custom pin assignment
    reset_6 = 0  # node 6   # custom pin assignment
    reset_7 = 0  # node 7   # custom pin assignment
    reset_8 = 0  # node 8   # custom pin assignment
else:
    reset_1 = 12  # node 1   # default 12
    reset_2 = 16  # node 2   # default 16
    reset_3 = 20  # node 3   # default 20
    reset_4 = 21  # node 4   # default 21
    reset_5 = 6  # node 5   # default 6
    reset_6 = 13  # node 6   # default 13
    reset_7 = 19  # node 7   # default 19
    reset_8 = 26  # node 8   # default 26

reset_list = [str(reset_1), str(reset_2), str(reset_3), str(reset_4),
              str(reset_5), str(reset_6), str(reset_7), str(reset_8)]

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']

if not linux_testing:
    import RPi.GPIO as GPIO  # only for Raspberry

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_2, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_3, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_4, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_5, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_6, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_7, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(reset_8, GPIO.OUT, initial=GPIO.HIGH)


    def all_pins_low():
        GPIO.output(reset_1, GPIO.LOW)
        GPIO.output(reset_2, GPIO.LOW)
        GPIO.output(reset_3, GPIO.LOW)
        GPIO.output(reset_4, GPIO.LOW)
        GPIO.output(reset_5, GPIO.LOW)
        GPIO.output(reset_6, GPIO.LOW)
        GPIO.output(reset_7, GPIO.LOW)
        GPIO.output(reset_8, GPIO.LOW)
        sleep(0.05)


    def all_pins_high():
        GPIO.output(reset_1, GPIO.HIGH)
        GPIO.output(reset_2, GPIO.HIGH)
        GPIO.output(reset_3, GPIO.HIGH)
        GPIO.output(reset_4, GPIO.HIGH)
        GPIO.output(reset_5, GPIO.HIGH)
        GPIO.output(reset_6, GPIO.HIGH)
        GPIO.output(reset_7, GPIO.HIGH)
        GPIO.output(reset_8, GPIO.HIGH)
        sleep(0.05)


    def all_pins_reset():
        all_pins_low()
        sleep(0.1)
        all_pins_high()


    def reset_gpio():
        all_pins_reset()
        GPIO.output((reset_list[i]), GPIO.LOW)
        sleep(0.1)
        GPIO.output((reset_list[i]), GPIO.HIGH)

if linux_testing:

    for i in range(0, 7):
        print("GPIO.setup(" + (reset_list[i]) + ", GPIO.OUT, initial=GPIO.HIGH)")
    sleep(0.5)


    def all_pins_reset():
        print("\n\n\t\t\tall_pins_reset")
        print("\n\t\t\t\t\t Linux - PC\n\n")
        sleep(0.3)


    def all_pins_low():
        print("\n\n\t\t\tall_pins_low")
        for i in range(0, 7):
            print("GPIO.output(" + (reset_list[i]) + ", GPIO.LOW")
        sleep(3)


    def all_pins_high():
        print("\n\n\tall_pins_high:")
        for i in range(0, 7):
            print("GPIO.output(" + (reset_list[i]) + ", GPIO.HIGH")
        sleep(3)


    def reset_gpio():
        print("GPIO.output(" + (reset_list[i]) + ", GPIO.LOW)")
        sleep(0.5)
        print("GPIO.output(" + (reset_list[i]) + ", GPIO.HIGH)")


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
    for i in range(0, nodes_number):
        all_pins_high()
        reset_gpio()
        print(reset_list[i])
        os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                  + user + "/RH-ota/firmware/" + firmware_version + "/node_" + str(i + 1) + ".hex:i ")
        print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
              + user + "/RH-ota/firmware/" + firmware_version + "/node_" + str(i + 1) + ".hex:i ")
        print("\n\n\t\t\t\t" + Bcolors.BOLD + "Node " + str(i + 1) + " - flashed" + Bcolors.ENDC + "\n\n")
        sleep(1)


def flash_all_gnd():
    for i in range(0, nodes_number):
        all_pins_high()
        reset_gpio()
        print(reset_list[i])
        os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                  + user + "/RH-ota/firmware/" + firmware_version + "/node_0.hex:i ")
        print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
              + user + "/RH-ota/firmware/" + firmware_version + "/node_0.hex:i ")
        print("\n\n\t\t\t\t" + Bcolors.BOLD + "Node " + str(i + 1) + " - flashed" + Bcolors.ENDC + "\n\n")
        sleep(1)


def flash_all_blink():
    for i in range(0, nodes_number):
        all_pins_high()
        reset_gpio()
        print(reset_list[i])
        os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                  + user + "/RH-ota/firmware/blink.hex:i ")
        print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
              + user + "/RH-ota/firmware/blink.hex:i ")
        print("\n\n\t\t\t\t" + Bcolors.BOLD + "Node " + str(i + 1) + " - flashed" + Bcolors.ENDC + "\n\n")
        sleep(1)


def node_x_menu(config, x):
    while True:
        print(Bcolors.BOLD + "\n\t\t\t\t Node " + str(x) + " selected" + Bcolors.ENDC)
        print(Bcolors.BOLD + "\n\n\t\t Choose flashing type:\n" + Bcolors.ENDC)
        print("\t\t 1 - " + Bcolors.GREEN + "Node gets own dedicated firmware - recommended" + Bcolors.ENDC)
        print("\t\t 2 - Node ground-auto selection firmware")
        print("\t\t 3 - Flashes 'Blink' on the node")
        print("\t\t 4 - Abort")
        selection = input()
        if selection == '1':
            all_pins_high()
            reset_gpio()
            if not linux_testing:
                os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                 flash:w:/home/" + user + "/RH-ota/firmware/" + firmware_version + "/node_" + str(x) + ".hex:i ")
            else:
                print("\t\t\t/home/" + user + "/RH-ota/firmware/" + firmware_version + "/node_" + str(x) + ".hex:i ")
            print(Bcolors.BOLD + "\n\t Node " + str(x) + " flashed\n" + Bcolors.ENDC)
            sleep(1)
            return
        if selection == '2':
            all_pins_high()
            reset_gpio()
            os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                      + user + "/RH-ota/firmware/" + firmware_version + "/node_0.hex:i")
            print(Bcolors.BOLD + "\n\t Node " + str(x) + " flashed\n" + Bcolors.ENDC)
            sleep(1)
            return
        if selection == '3':
            all_pins_high()
            reset_gpio()
            os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/" + user + "/RH-ota/firmware/" + firmware_version + "/blink.hex:i ")
            print(Bcolors.BOLD + "\n\t Node " + str(x) + " flashed\n" + Bcolors.ENDC)
            sleep(1)
            return
        if selection == '4':
            node_menu(config)
        else:
            continue


def node_menu(config):
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
        selection = input("\n\n\t\t" + Bcolors.BOLD + "Which node do you want to program:" + Bcolors.ENDC + " ")
        print("\n\n")
        if (selection.isdigit()) and int(selection) <= 8:
            x = selection
            sleep(0.1)
            node_x_menu(config, x)
        if selection == 'e':
            break
        else:
            continue


def gpio_state(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    print("\n\n\n")  # todo end every other line with logo_top()
    os.system("echo " + str(reset_1) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_2) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_3) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_4) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_5) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_6) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_7) + " > /sys/class/GPIO/unexport")
    os.system("echo " + str(reset_8) + " > /sys/class/GPIO/unexport")
    os.system("echo 19 > /sys/class/GPIO/unexport")
    os.system("echo 20 > /sys/class/GPIO/unexport")
    os.system("echo 21 > /sys/class/GPIO/unexport")
    print("\n\n        DONE\n\n")
    sleep(0.3)


def nodes_update(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        node_menu_content = """\n
                            {bold}{underline}CHOOSE FLASHING TYPE:{endc}

                    {green}{bold}1 - Every Node gets own dedicated firmware - rec.{endc}

                    2 - Nodes will use ground-auto selection firmware

                    3 - Flash 'Blink' on every node

                    4 - Flash each node individually

                    5 - Fix GPIO pins state 

                    e - Exit to main menu

                    {yellow}e - Exit to main menu{endc}
            """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                       endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
        print(node_menu_content)
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
            node_menu(config)
        if selection == '5':
            gpio_state(config)
        if selection == 'e':
            break
        else:
            continue


def main():
    config = load_config()
    nodes_update(config)


if __name__ == "__main__":
    main()

# def connectionTest():
# nodeOneReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 1:
# return
# nodeTwoReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 2:
# return
# nodeThreeReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 3:
# return
# nodeFourReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 4:
# return
# nodeFiveReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 5:
# return
# nodeSixReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 6:
# return
# nodeSevenReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 7:
# return
# nodeEightReset()
# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
# sleep(2)
# if nodes_number == 8:
# return
