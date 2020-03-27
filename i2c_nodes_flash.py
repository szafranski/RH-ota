from time import sleep
import os
import sys
import json
from modules import clear_the_screen, Bcolors, logo_top
try:
    from smbus import SMBus
except ModuleNotFoundError as module_err:
    print(module_err)
    print("For flashing purposes you have to use smbus module")
    sleep(2)

# from modules import RH_version  # invalid syntax for some reason
# todo cannot find reference for RH_version error shows

RH_version = 'master'

firmware_version = RH_version

i2c_error_msg = "\nI2C communication doesn't work properly"
err_time = 1

try:
    bus = SMBus(1)  # indicates /dev/ic2-1
except PermissionError:
    print('SMBus(1) - error')
    print(i2c_error_msg)
    sleep(err_time)
except NameError as name_error:
    print('SMBus(1) - error')
    print(name_error)
    print(i2c_error_msg)

sleepAmt = 1

on = [1]
off = [0]

reset_mate_node_command = 0x79
disable_serial_on_the_node_command = 0x80


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return checksum


'''nodes I2C adresses'''

#  node     hex     RH
node1addr = 0x08  # 8
node2addr = 0x0a  # 10
node3addr = 0x0c  # 12
node4addr = 0x0e  # 14
node5addr = 0x10  # 16
node6addr = 0x12  # 18
node7addr = 0x14  # 20
node8addr = 0x16  # 22

addr_list_int = [node1addr, node2addr, node3addr, node4addr,
                 node5addr, node6addr, node7addr, node8addr]

addr_list = [str(item) for item in addr_list_int]


def disable_serial_on_the_node(addr):  # todo Michael has to tell
    sleep(sleepAmt)
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    # bus.write_byte(addr, disable_serial_on_the_node)
    bus.write_i2c_block_data(addr, disable_serial_on_the_node, on)
    # bus.write_i2c_block_data(addr, disable_serial_on_the_node, off)
    print("serial communication disabling - done")
    sleep(sleepAmt)


def disable_serial_on_all_nodes(addr):
    disable_serial_on_the_node()
    bus.write_i2c_block_data(addr, disable_serial_on_the_node, [])


def reset_mate_node():
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, off)
    print("off sent")
    print("node reset in progress")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(0.2)


def flash_blink(user):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{user}/RH-ota/firmware/blink.hex:i")


def flash_firmware(user, firmware_version):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/node_0.hex:i")


if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

nodes_number = data['nodes_number']

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']

gpio_reset_pin = 12

try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
    # ensures nothing is being reset during program start
except ModuleNotFoundError:
    print("GPIO import - failed")
    sleep(2)


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


if not linux_testing:
    def disable_serial_on_all_nodes(nodes_number):
        for i in range(1, nodes_number):
            bus.write_byte(addr_list[i], disable_serial_on_the_node_command)

'''commands needed for interacion with nodes using GPIO pins '''


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


def reset_mate_node(addr):
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, off)
    print("RESET command - sent")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("pin at default state - sent\n")
    sleep(0.2)


def flash_firmware_onto_all_nodes_with_auto_addr():
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes()
        reset_mate_node()
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{firmware_version}/node_0.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/i2c/{firmware_version}/node_{i}.hex:i")
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_blink_onto_all_gnd_nodes():
    for i in range(1, nodes_number):
        disable_serial_on_all_nodes()
        reset_mate_node()
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{user}\
        /RH-ota/firmware/{firmware_version}/blink.hex:i")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/blink.hex:i ")
    print(f"\n\n\t\t\t\t{Bcolors.BOLD}Node {i} - flashed{Bcolors.ENDC}\n\n")
    sleep(1)


def flash_nodes_individually():
    def node_selection_menu():
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

    def flash(port):
        for i in range(nodes_num):
            input("Hit any key and push reset key of next node after 1 second")
            sleep(0.2)
            disable_serial_on_all_nodes()
            os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/tty{port} -b 57600 -U \
                    flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/node_0.hex:i")

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


def main():
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
        flash_firmware_onto_all_gnd_nodes()
        logo_update()
    if selection == '2':
        flash_nodes_individually()
        logo_update()
    if selection == '3':
        first_flashing(nodes_number)
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
        main()


if __name__ == "__main__":
    main()
