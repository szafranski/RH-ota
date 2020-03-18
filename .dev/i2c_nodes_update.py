from smbus import SMBus
from time import sleep
import os
import sys
import json

if os.path.exists("./updater-config.json") == True:
    with open('updater-config.json') as config_file:
        data = json.load(config_file)
else:
    with open('distr-updater-config.json') as config_file:
        data = json.load(config_file)

if data['debug_mode'] == 1:
    linux_testing = True
else:
    linux_testing = False 

if linux_testing == True:
    user = data['debug_user']
else:
    user = data['pi_user']
preffered_RH_version = data['RH_version']

if preffered_RH_version == 'master':
    firmware_version = 'master'
if preffered_RH_version == 'beta':
    firmware_version = 'beta'
if preffered_RH_version == 'stable':
    firmware_version = 'stable'
if preffered_RH_version == 'custom':
    firmware_version = 'stable'

bus = SMBus(1) # indicates /dev/ic2-1

node1addr = 0x08
node2addr = 0x10
node3addr = 0x12
node4addr = 0x14
node5addr = 0x16
node6addr = 0x18
node7addr = 0x20
node8addr = 0x22

reset_1=12

if (linux_testing == False): 
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
    GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.HIGH)

    def allPinsLow():
        GPIO.output(reset_1, GPIO.LOW)
        # GPIO.output(reset_2, GPIO.LOW)
        # GPIO.output(reset_3, GPIO.LOW)
        # GPIO.output(reset_4, GPIO.LOW)
        # GPIO.output(reset_5, GPIO.LOW)
        # GPIO.output(reset_6, GPIO.LOW)
        # GPIO.output(reset_7, GPIO.LOW)
        # GPIO.output(reset_8, GPIO.LOW)
        sleep(0.05)

    def allPinsHigh():
        GPIO.output(reset_1, GPIO.HIGH)
        # GPIO.output(reset_2, GPIO.HIGH)
        # GPIO.output(reset_3, GPIO.HIGH)
        # GPIO.output(reset_4, GPIO.HIGH)
        # GPIO.output(reset_5, GPIO.HIGH)
        # GPIO.output(reset_6, GPIO.HIGH)
        # GPIO.output(reset_7, GPIO.HIGH)
        # GPIO.output(reset_8, GPIO.HIGH)
        sleep(0.05)

    def allPinsReset():
        GPIO.output(reset_1, GPIO.LOW)
        # GPIO.output(reset_2, GPIO.LOW)
        # GPIO.output(reset_3, GPIO.LOW)
        # GPIO.output(reset_4, GPIO.LOW)
        # GPIO.output(reset_5, GPIO.LOW)
        # GPIO.output(reset_6, GPIO.LOW)
        # GPIO.output(reset_7, GPIO.LOW)
        # GPIO.output(reset_8, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_1, GPIO.HIGH)
        # GPIO.output(reset_2, GPIO.HIGH)
        # GPIO.output(reset_3, GPIO.HIGH)
        # GPIO.output(reset_4, GPIO.HIGH)
        # GPIO.output(reset_5, GPIO.HIGH)
        # GPIO.output(reset_6, GPIO.HIGH)
        # GPIO.output(reset_7, GPIO.HIGH)
        # GPIO.output(reset_8, GPIO.HIGH)

    def nodeOneReset():
        allPinsHigh()
        GPIO.output(reset_1, GPIO.LOW)
        sleep(0.1)
        GPIO.output(reset_1, GPIO.HIGH)
    def nodeTwoReset():
        bus.write_byte(node1addr, 0x8)
        # sleep(0.1)
        # bus.write_byte(node1addr, 0x1)
    def nodeThreeReset():
        bus.write_byte(node2addr, 0x0)
        sleep(0.1)
        bus.write_byte(node2addr, 0x1)
    def nodeFourReset():
        bus.write_byte(node3addr, 0x0)
        sleep(0.1)
        bus.write_byte(node3addr, 0x1)
    def nodeFiveReset():
        bus.write_byte(node4addr, 0x0)
        sleep(0.1)
        bus.write_byte(node4addr, 0x1)
    def nodeSixReset():
        bus.write_byte(node5addr, 0x0)
        sleep(0.1)
        bus.write_byte(node5addr, 0x1)
    def nodeSevenReset():
        bus.write_byte(node6addr, 0x0)
        sleep(0.1)
        bus.write_byte(node6addr, 0x1)
    def nodeEightReset():
        bus.write_byte(node7addr, 0x0)
        sleep(0.1)
        bus.write_byte(node7addr, 0x1)

def test():
    selection=str(raw_input("What do you want to send?"))
    if selection=='0':
        bus.write_byte(node1addr, 0x0) # switch it off
        test()
    if selection=='1':
        bus.write_byte(node1addr, 0x1) # switch it on
        test()
    if selection=='2':
        nodeTwoReset()
        os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/comm.hex:i ")
        print("\n\t Node flashed using I2C resetting - blink\n")
        sleep(1.5)
        test()
    if selection=='3':
        sys.exit()
test()


