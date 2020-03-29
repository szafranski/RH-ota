from time import sleep
import os
import sys
from modules import clear_the_screen, Bcolors, logo_top
from conf_wizard_ota import conf_ota
error_msg = "SMBus(1) - error\nI2C communication doesn't work properly"
err_time = 1
try:
    from smbus import SMBus
    bus = SMBus(1)  # indicates /dev/ic2-1
    return bus
except PermissionError as perm_error:
    print(error_msg)
    print(perm_error)
    sleep(err_time)
except NameError as name_error:
    print(error_msg)
    print(name_error)
    sleep(err_time)

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
    # ensures nothing is being reset during program's start
except ModuleNotFoundError:
    print("GPIO import - failed")
    sleep(2)

def i2c_data():
    sleep_amt = 1
    disable_serial_data = [0]
    on = [1]
    off = [0]
    reset_mate_node_command = 0x79
    disable_serial_on_the_node_command = 0x80

    return sleep_amt, disable_serial_data, on, off, reset_mate_node_command, disable_serial_on_the_node_command


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return checksum


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


def reset_mate_node():
    sleep_amt = 1
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, off)
    print("off sent")
    print("node reset in progress")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(0.2)


def flash_blink(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i")


def flash_firmware(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/{config.firmware_version}/node_0.hex:i")


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


def disable_serial_on_the_node(addr, disable_serial_data, disable_serial_on_the_node_command):
    disable_serial_data.append(calculate_checksum(disable_serial_data))
    bus.write_i2c_block_data(addr, disable_serial_on_the_node_command, disable_serial_data)


def disable_serial_on_all_nodes(nodes_number, disable_serial_on_the_node_command):
    for i in range(1, nodes_number):
        bus.write_byte(nodes_addresses()[i], disable_serial_on_the_node_command)


'''commands needed for interaction with nodes using GPIO pins '''


def gpio_reset_pin_low(gpio_reset_pin):
    GPIO.output(gpio_reset_pin, GPIO.LOW)
    sleep(0.1)


def gpio_reset_pin_high(gpio_reset_pin):
    GPIO.output(gpio_reset_pin, GPIO.HIGH)
    sleep(0.1)


def reset_gpio_pin():
    gpio_reset_pin_high()
    gpio_reset_pin_low()
    gpio_reset_pin_high()


def reset_mate_node(i2c_data, addr):
    on, off, sleep_amt, reset = i2c_data()
    on.append(calculate_checksum(on))  # todo it should use values from i2c_data() - error :(
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, off)
    print("RESET command - sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(0.2)


def flash_firmware_onto_all_nodes_with_auto_addr(user, nodes_number):
    i = 1
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes()
        reset_mate_node()
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{firmware_version}/node_0.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{firmware_version}/node_{i}.hex:i")
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_blink_onto_all_gnd_nodes(config, nodes_number):
    i = 1
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes()
        reset_mate_node()
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{config.user}\
        /RH-ota/firmware/{firmware_version}/blink.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{config.user}/RH-ota/firmware/{config.firmware_version}/blink.hex:i ")
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
            node_one_reset()  # todo change to reset and serial disabling
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/node_0.hex:i")
            print(f"{Bcolors.BOLD}\n\t Node {str(selected_node_number)} flashed\n{Bcolors.ENDC}")
            sleep(1.5)
            return
        if selection == '2':
            node_one_reset()
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/{user}/RH-ota/firmware/blink.hex:i ")
            print(f"{Bcolors.BOLD}\n\t Node {str(selected_node_number)} flashed\n{Bcolors.ENDC}")
            sleep(1.5)
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


def fashing_menu(config):
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
