from time import sleep
import os
import sys
import json
from modules import clear_the_screen, Bcolors, logo_top
from smbus import SMBus  # works only on Pi
from modules import RH_version #  invalid syntax for some reason


firmware_version = RH_version
#  todo check if it is ok? implement firmware version reading to modules.py

bus = SMBus(1)  # indicates /dev/ic2-1


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

if not linux_testing:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
    # ensures nothing is being reset during program start


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



node1addr = 0x08  # 8
node2addr = 0x0a  # 10
node3addr = 0x0c  # 12
node4addr = 0x0e  # 14
node5addr = 0x12  # 16
node6addr = 0x14  # 18
node7addr = 0x14  # 20
node8addr = 0x16  # 22

# address have to be compatible with RH addressing scheme

gpio_reset_pin = 12  # GPIO pin 12 - nothing to do with nodes pin 12

RESET_MATE_NODE = 0x79
DISABLE_SERIAL = 0x80

def flash_firmware_onto_numbered_node():
    os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
        + user + "/RH-ota/firmware/i2c/reset_no_s.hex:i")

if not linux_testing:

    def disable_serial_on_all_nodes():
        bus.write_byte(node1addr, DISABLE_SERIAL)
        bus.write_byte(node2addr, DISABLE_SERIAL)
        bus.write_byte(node3addr, DISABLE_SERIAL)
        bus.write_byte(node4addr, DISABLE_SERIAL)
        bus.write_byte(node5addr, DISABLE_SERIAL)
        bus.write_byte(node6addr, DISABLE_SERIAL)
        bus.write_byte(node7addr, DISABLE_SERIAL)
        bus.write_byte(node8addr, DISABLE_SERIAL)

    def gpio_reset_pin_low():
        GPIO.output(gpio_reset_pin, GPIO.LOW)
        sleep(0.1)

    def gpio_reset_pin_high():
        GPIO.output(gpio_reset_pin, GPIO.HIGH)
        sleep(0.1)

    #  all reset commands have disabling serial on all nodes function implemented - for now

    def node_one_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node2addr, RESET_MATE_NODE)  # node 2 resets node 1
        sleep(0.1)

    def node_two_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node1addr, RESET_MATE_NODE)  # node 1 resets node 2
        sleep(0.1)

    def node_three_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node4addr, RESET_MATE_NODE)  # node 4 resets node 3
        sleep(0.1)

    def node_four_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node3addr, RESET_MATE_NODE)  # node 3 resets node 4
        sleep(0.1)

    def node_five_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node6addr, RESET_MATE_NODE)  # node 6 resets node 5
        sleep(0.1)

    def node_six_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node5addr, RESET_MATE_NODE)  # node 5 resets node 6
        sleep(0.1)

    def node_seven_reset():
        disable_serial_on_all_nodes()
        bus.write_byte(node8addr, 0x79)  # node 8 resets node 7
        sleep(0.1)

    def node_eight_reset():
        bus.write_byte(node7addr, 0x79)  # node 7 resets node 8
        sleep(0.1)


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


flash_firmware_onto_8_nodes()


def flash_firmware_onto_all_gnd_nodes():
    global i
    for i in range(0, nodes_number):
        # all_pins_high()
        # reset_gpio()
        # print(reset_list[i])
        node_one_reset()   #  todo iterate one, two, three etc.
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{user}\
        /RH-ota/firmware/i2c/{firmware}/node_0.hex:i ").format(firmware=firmware_version)
        print(f"""avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{user}\
        /RH-ota/firmware/i2c/{firmware}/node_{i+1}.hex:i """.format(user=user, firmware=firmware_version))
        print(f"\n\n\t\t\t\t{bold}Node {i+1} - flashed{endc}\n\n".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC))
        sleep(1)



def flash_blink_onto_all_gnd_nodes():
    global i
    for i in range(0, nodes_number):
        # all_pins_high()
        # reset_gpio()
        # print(reset_list[i])
        node_one_reset()   #  todo iterate one, two, three etc.
        os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{user}\
        /RH-ota/{firmware}/i2c/blink.hex:i ").format(firmware=firmware_version)
        print(f"""avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{user}\
        /RH-ota/firmware/i2c/blink.hex:i """.format(user=user)
        print(f"""\n\n\t\t\t\t{bold}Node {(i+1)} - flashed{endc}\n\n""".format(bold=Bcolors.BOLD, endc=Bcolors.ENDC))
        sleep(1)


def flash_each_node():
    def node_x_menu():
        global x
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
            node_menu()
        if selection == 'dev':
            all_pins_high()
            reset_gpio()
            os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
            flash:w:/home/" + user + "/RH-ota/.dev/node_" + str(x) + ".hex:i ")
            print(Bcolors.BOLD + "\n\t Testing firmware on Node " + str(x) + " flashed\n" + Bcolors.ENDC)
            sleep(1)
        else:
            node_x_menu()

    def node_menu():
        global x
        clear_the_screen()
        logo_top()
        sleep(0.05)
        print("\n\n\n\t\t\t\t    " + Bcolors.RED + Bcolors.BOLD + "NODES MENU" + Bcolors.ENDC)
        print("\n\t\t " + Bcolors.BOLD + "1 - Flash node 1 \t\t 5 - Flash node 5" + Bcolors.ENDC)
        print("\n\t\t " + Bcolors.BOLD + "2 - Flash node 2 \t\t 6 - Flash node 6" + Bcolors.ENDC)
        print("\n\t\t " + Bcolors.BOLD + "3 - Flash node 3 \t\t 7 - Flash node 7" + Bcolors.ENDC)
        print("\n\t\t " + Bcolors.BOLD + "4 - Flash node 4 \t\t 8 - Flash node 8")
        print("\n\t\t\t\t" + Bcolors.YELLOW + Bcolors.BOLD + "e - Exit to main menu" + Bcolors.ENDC)
        selection = input("\n\n\t\t" + Bcolors.BOLD + "Which node do you want to program:" + Bcolors.ENDC + " ")
        print("\n\n")
        if (selection.isdigit()) and int(selection) <= 8:
            x = selection
            sleep(0.5)
            node_x_menu()
        if selection == 'e':
            nodes_update()
        else:
            node_menu()

    node_menu()


def gpio_state():
    clear_the_screen()
    logo_top()
    print("\n\n\n")
    os.system("echo " + gpio_reset_pin + " > /sys/class/GPIO/unexport")
    print("\n\n        DONE\n\n")
    sleep(0.3)


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
    logo_top()
    sleep(0.05)
    print("\n\n\t\t\t " + Bcolors.BOLD + Bcolors.UNDERLINE + "CHOOSE FLASHING TYPE:\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.GREEN + Bcolors.BOLD + "1 - Every Node gets own dedicated firmware - recommended\n"
          + Bcolors.ENDC)
    print("\t\t " + Bcolors.BOLD + "2 - Nodes will use ground-auto selection firmware\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.BOLD + "3 - Flash 'Blink' on every node\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.BOLD + "4 - Flash each node individually\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.BOLD + "5 - I2C programming - early beta\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.BOLD + "6 - Fix GPIO pins state - obsolete\n" + Bcolors.ENDC)
    print("\t\t " + Bcolors.YELLOW + Bcolors.BOLD + "e - Exit to main menu\n" + Bcolors.ENDC)
    sleep(0.3)
    selection = input()
    if selection == '1':
        flash_firmware_onto_all_gnd_nodes()
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
        os.system("python ./.dev/i2c_nodes_py")
    if selection == '6':
        gpio_state()
    if selection == 'e':
        sys.exit()
    else:
        nodes_update()


nodes_update()


## testing leftovers:

def flashing():
    input("Ok?")
    bus.write_byte(node1addr, 0x79)
    sleep(0.5)
    os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
              + user + "/RH-ota/firmware/reset_no_s.hex:i")
    sleep(1)
    bus.write_byte(node2addr, 0x79)
    sleep(0.5)
    os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
              + user + "/RH-ota/firmware/reset_no_s.hex:i")
    sleep(1)


# flashing()

#  sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/pi/RH-ota/firmware/reset_no_s.hex:i

def test():
    selection = input("What do you want to send?")
    if selection == '0':
        bus.write_byte(node1addr, 0x0)  # switch it off
        test()
    if selection == '1':
        bus.write_byte(node1addr, 0x1)  # switch it on
        test()
    if selection == '2':
        node_two_reset()
        os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                  + user + "/RH-ota/comm.hex:i ")
        print("\n\t Node flashed using I2C resetting - blink\n")
        sleep(1.5)
        test()
    if selection == '3':
        sys.exit()

# test()
