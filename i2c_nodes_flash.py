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

i2c_error_msg = "\nI2C communication will not work"
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

#  node     real   RH 

node1addr = 0x08  # 8
node2addr = 0x0a  # 10
node3addr = 0x0c  # 12
node4addr = 0x0e  # 14
node5addr = 0x10  # 16
node6addr = 0x12  # 18
node7addr = 0x14  # 20
node8addr = 0x16  # 22

addr_list = ['0x08', '0x0a', '0x0c', '0x0e', '0x10', '0x12', '0x14', '0x16']

def disable_serial_on_the_node(): # todo Michael has to tell :(
    sleep(sleepAmt)
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    # bus.write_byte(addr, disable_serial_on_the_node)
    bus.write_i2c_block_data(addr, disable_serial_on_the_node, on)
    # bus.write_i2c_block_data(addr, disable_serial_on_the_node, off)
    print("serial communication disabling - done")
    sleep(sleepAmt)


def disable_serial_on_all_nodes():
    disable_serial_on_the_node()
    bus.write_i2c_block_data(addr, disable_serial_on_the_node, on)


def reset_mate_node():
    disable_serial_on_the_node()
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


def flash_node_blink():
    os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/pi/RH-ota/firmware/blink.hex:i")

def flash_node_firmware():
    os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/pi/RH-ota/firmware/{firmware_versionm}/node_0.hex:i")


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


def logo_update():
    print("""
    #######################################################################
    #                                                                     #
    #{bold}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s}#
    #                                                                     #
    #              {bold}         Thank you!        {endc}                #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=nodes_number, bold=Bcolors.BOLD_S, endc=Bcolors.ENDC_S, s=10 * ' '))



def flash_firmware_onto_numbered_node():
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{user}/RH-ota/firmware/i2c/reset_no_s.hex:i")


if not linux_testing:
    def disable_serial_on_all_nodes(nodes_number):
        for i in range(1, nodes_number):
            bus.write_byte(addr_list[i], disable_serial_on_the_node_command)


'''commands needed for interacion with nodes using GPIO pins '''
   
    def gpio_reset_pin_low():
        GPIO.output(gpio_reset_pin, GPIO.LOW)
        sleep(0.1)


    def gpio_reset_pin_high():
        GPIO.output(gpio_reset_pin, GPIO.HIGH)
        sleep(0.1)


    def reset_gpio_pin():
        gpio_reset_pin_high()
        gpio_reset_pin_low()
        gpio_reset_pin_high()



''' those below may be redundant '''

    def node_one_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node2addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node2addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node2addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_two_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node1addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node1addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node1addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_three_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node4addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node4addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node4addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_four_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node3addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node3addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node3addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_five_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node6addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node6addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node6addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_six_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node5addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node5addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node5addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_seven_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node8addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node8addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node8addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


    def node_eight_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node7addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node7addr, RESET_MATE_NODE_LOW)  # node 2 resets node 1
        sleep(1)
        bus.write_byte(node7addr, RESET_MATE_NODE_HIGH)  # node 2 resets node 1
        sleep(0.1)


''' end of redundant? '''


''' below - tests'''

def flash_firmware_onto_8_nodes():
    selection = input("All nodes will be flashed. Ok? Hit 'y'")  # hit enter before start
    if selection == 'y':
        node_one_reset()
        flash_firmware_onto_numbered_node()
        node_two_reset()
        flash_firmware_onto_numbered_node()
        node_three_reset()
        flash_firmware_onto_numbered_node()
        node_four_reset()
        flash_firmware_onto_numbered_node()
        node_five_reset()
        flash_firmware_onto_numbered_node()
        node_six_reset()
        flash_firmware_onto_numbered_node()
        node_seven_reset()
        flash_firmware_onto_numbered_node()
        node_eight_reset()
        flash_firmware_onto_numbered_node()
    else:
        flash_firmware_onto_8_nodes()


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


def flash_each_node():
    def node_x_menu():
        global x
        flash_each_node_menu = """ {bold}
                
                Node {x} selected
        
                    Choose flashing type:
                
            1 - Node gets own dedicated firmware - recommended
        
            2 - Node ground-auto selection firmware
        
            3 - Flashes 'Blink' on the node
        
            4 - Abort
        
        """.format(x=str(x), bold=Bcolors.BOLD, endc=Bcolors.ENDC)
        print(flash_each_node_menu)
        selection = input()
        if selection == '1':
            reset_gpio_pin()
            if not linux_testing:
                os.system(f"echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
                 flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/node_{str(x)}.hex:i ")
            else:
                print(f"\t\t\t/home/{user}/RH-ota/firmware/{firmware_version}/node_{str(x)}.hex:i ")
                print(f"{Bcolors.BOLD}\n\t Node {str(x)}flashed\n{Bcolors.ENDC}")
                sleep(1)
                return
        if selection == '2':
            reset_gpio_pin()
            os.system(f"echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/node_0.hex:i")
            print(f"{Bcolors.BOLD}\n\t Node {str(x)}flashed\n{Bcolors.ENDC}")
            sleep(1)
            return
        if selection == '3':
            reset_gpio_pin()
            os.system(f"echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/{user}/RH-ota/firmware/{firmware_version}/blink.hex:i ")
            print(f"{Bcolors.BOLD}\n\t Node {str(x)}flashed\n{Bcolors.ENDC}")
            sleep(1)
            return
        if selection == '4':
            node_menu()
        else:
            node_x_menu()

    def node_menu():
        clear_the_screen()
        logo_top()
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
        selection = input(f"\n\n\t\t{Bcolors.BOLD}Which node do you want to program:{Bcolors.ENDC} ")
        print("\n\n")
        if selection.isdigit() and int(selection) <= 8:
            x = selection
            sleep(0.5)
            node_x_menu()
        if selection == 'e':
            nodes_update()
        else:
            node_menu()

    node_menu()


def reset_gpio_state():
    clear_the_screen()
    logo_top()
    print("\n\n\n")
    os.system(f"echo {gpio_reset_pin} > /sys/class/GPIO/unexport")
    print("\n\n\t\t\tDONE\n\n")
    sleep(0.5)          


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

def nodes_update():
    clear_the_screen()
    logo_top(linux_testing)
    sleep(0.05)
    node_menu = """\n
                        {bold}{underline}CHOOSE FLASHING TYPE:{endc}

                {green}{bold}1 - Flash each node automatically - rec.{endc}

                {bold}2 - Flash 'Blink' on every node

                3 - Flash each node individually

                4 - Show I2C connected devices

                5 - Flash using GPIO reset pins - obsolete

                6 - Fix GPIO pins state - obsolete

                {yellow}'e' - Exit to main menu{endc}
        """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                   endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
    print(node_menu)
    sleep(0.1)
    selection = input()
    if selection == '1':
        flash_firmware_onto_all_gnd_nodes()
        logo_update()
        sleep(3)
    if selection == '2':
        flash_blink_onto_all_gnd_nodes()
        logo_update()
        sleep(3)
    if selection == '3':
        flash_each_node()
        logo_update()
        sleep(3)
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
        nodes_update()


nodes_update()


