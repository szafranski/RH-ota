from smbus import SMBus  # works only on Pi
from time import sleep
import os
import sys
import json

if os.path.exists("./updater-config.json"):
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

RESET_MATE_NODE = 0x79
DISABLE_SERIAL = 0x80

if data['debug_mode']:
    linux_testing = True
else:
    linux_testing = False

if linux_testing:
    user = data['debug_user']
else:
    user = data['pi_user']
preferred_RH_version = data['RH_version']

if preferred_RH_version == 'master':
    firmware_version = 'master'
if preferred_RH_version == 'beta':
    firmware_version = 'beta'
if preferred_RH_version == 'stable':
    firmware_version = 'stable'
if preferred_RH_version == 'custom':
    firmware_version = 'stable'

bus = SMBus(1)  # indicates /dev/ic2-1

node1addr = 0x08
node2addr = 0x0a
node3addr = 0x0c
node4addr = 0x0e
node5addr = 0x16
node6addr = 0x18
node7addr = 0x20
node8addr = 0x22

# address have to be compatible with RH addressing scheme

gpio_reset_pin = 12  # GPIO pin 12 - nothing to do with nodes pin 12


def flash_numbered_node():
    os.system(
        "sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
        + user + "/RH-ota/firmware/i2c/reset_no_s.hex:i")


if not linux_testing:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    GPIO.setup(gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)  # ensures nothing is being reset during program start


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


def flash_all_nodes():
    input("All nodes will be flashed. Ok? Hit 'Enter'")  # hit enter before start
    node_one_reset()
    flash_numbered_node()
    node_two_reset()
    flash_numbered_node()
    node_three_reset()
    flash_numbered_node()
    node_four_reset()
    flash_numbered_node()
    node_five_reset()
    flash_numbered_node()
    node_six_reset()
    flash_numbered_node()
    node_seven_reset()
    flash_numbered_node()
    node_eight_reset()
    flash_numbered_node()


flash_all_nodes()


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
