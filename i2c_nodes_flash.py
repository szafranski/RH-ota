from time import sleep
import os
import sys
from modules import clear_the_screen, Bcolors, logo_top
from flash_common import flashing_steps, disable_serial_on_the_node
from conf_wizard_ota import conf_ota

error_msg = "SMBus(1) - error\nI2C communication doesn't work properly"
err_time = 1
try:
    from smbus import SMBus  # works only on Pi
    bus = SMBus(1)  # indicates /dev/ic2-1 - correct i2c bus for most Pies
except PermissionError as perm_error:
    print(error_msg)
    print(perm_error)
    sleep(err_time)
except NameError as name_error:
    print(error_msg)
    print(name_error)
    sleep(err_time)

try:
    import RPi.GPIO as GPIO  # works only on Pi
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(config.gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
    # ensures nothing is being reset during program's start
except ModuleNotFoundError:
    print("GPIO import - failed")
    sleep(2)


def nodes_addresses():
    """nodes I2C adresses - below: conversion to hex numbers required by SMBus module"""
    #  node    addr
    node1addr = 8
    node2addr = 10
    node3addr = 12
    node4addr = 14
    node5addr = 16
    node6addr = 18
    node7addr = 20
    node8addr = 22

    addr_list_int = [node1addr, node2addr, node3addr, node4addr,
                     node5addr, node6addr, node7addr, node8addr]

    addr_list_hex = [hex(item) for item in addr_list_int]

    addr_list = (str(item) for item in addr_list_hex)

    return addr_list


def logo_update(nodes_number):
    print("""
    #######################################################################
    #                                                                     #
    #{bold}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s}#
    #                                                                     #
    #              {bold}         Thank you!        {endc}                #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=nodes_number, bold=Bcolors.BOLD_S, endc=Bcolors.ENDC_S, s=10 * ' '))


def disable_serial_on_all_nodes(addr_list, nodes_number):
    for addr in addr_list:
        disable_serial_on_the_node(addr)
        sleep(2)
        if addr_list.index(addr) == nodes_number:
            break

def flash_firmware_onto_all_nodes_with_auto_addr(user, nodes_number, firmware_version, addr_list):
    for addr in addr_list:
        flashing_steps()
        sleep(2)
        if addr_list.index(addr) == nodes_number:
            break
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_blink_onto_all_gnd_nodes(user, nodes_number, firmware = blink, addr_list):
    for addr in addr_list:
        flashing_steps()
        sleep(2)
        if addr_list.index(addr) == nodes_number:
            break
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_nodes_individually():
    def node_selection_menu(config):
        clear_the_screen()
        logo_top(config.linux_testing)
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
        if int(selection) in range(8):
            selected_node_number = selection
            return selected_node_number
        if selection == 'e':
            main()
        else:
            node_selection_menu()

    def specific_node_menu(selected_node_number):
        print(f"""
        {Bcolors.BOLD}\n\t\t\tNode {str(selected_node_number)}  selected{Bcolors.ENDC}
                Choose flashing type:\n{Bcolors.ENDC}
        1 - {Bcolors.GREEN}Node ground-auto selection firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}
        2 - Flashes 'Blink' on the node - only for test purposes
        a - Abort{Bcolors.ENDC}""")
        selection = input()
        if selection == '1':
            flashing_steps()
            print(f"{Bcolors.BOLD}\n\t Node {str(selected_node_number)} flashed\n{Bcolors.ENDC}")
            sleep(1.5)
            return
        if selection == '2':
            flashing_steps()
            return
        if selection == 'a':
            specific_node_menu()
        if selection == 'dev':
            node_one_reset()
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/{user}/RH-ota/.dev/node_test.hex:i ")
            print(Bcolors.BOLD + "\n\t Testing firmware on Node " + str(
                selected_node_number) + " flashed\n" + Bcolors.ENDC)
            sleep(1.5)
        else:
            specific_node_menu()


def first_flashing(nodes_num):

    def flash(config, port):
        for i in range(nodes_num):
            input("Hit any key and push reset key of next node after 1 second")
            sleep(0.2)
            disable_serial_on_all_nodes()
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/tty{port} -b 57600 -U \
                    flash:w:/home/{config.user}/RH-ota/firmware/{config.firmware_version}/node_0.hex:i")

    while True:
        port_sel = input("UART or USB flashing [default: UART]")
        if port_sel.lower() == 'uart':
            port_sel = 'S0'
            flash(port_sel)
        if port_sel.lower() == 'usb':
            port_sel = 'USB0'
            flash(port_sel)
        else:
            print("Type: 'UART' or 'USB' ")


def reset_gpio_state():
    clear_the_screen()
    logo_top()
    print("\n\n\n")
    os.system(f"echo {gpio_reset_pin} > /sys/class/GPIO/unexport")
    print("\n\n\t\t\tDONE\n\n")
    sleep(0.5)


def connection_test(nodes_num):
    for i in range(nodes_num):
        disable_serial_on_all_nodes()
        os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
        sleep(0.2)


def flashing_menu(config):
    clear_the_screen()
    logo_top(linux_testing)
    sleep(0.05)
    node_menu = """\n
                        {bold}{underline}CHOOSE FLASHING TYPE:{endc}

                {green}{bold}1 - Flash each node automatically - rec.{endc}

                2 - Flash each node individually

                3 - Flash first time

                4 - Show I2C connected devices

                5 - Flash using GPIO reset pins - obsolete

                6 - Fix GPIO pin state

                {yellow}'e' - Exit to main menu{endc}
        """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                   endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
    print(node_menu)
    sleep(0.1)
    selection = input()
    if selection == '1':
        flash_firmware_onto_all_nodes_with_auto_addr()
        logo_update()
    if selection == '2':
        flash_nodes_individually()
        logo_update()
    if selection == '3':
        first_flashing(config.nodes_number)
        logo_update()
    if selection == '4':
        logo_top()
        os.system("i2cdetect - y 1")
    if selection == '5':
        os.system("python3 ./nodes_update_old.py")
    if selection == '6':
        reset_gpio_state()
    if selection == 'e':
        sys.exit()
    else:
        break


def main():
    fashing_menu()


if __name__ == "__main__":
    main()
