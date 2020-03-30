from time import sleep
import os
import sys


def communication_initializing():
    error_msg = "SMBus(1) - error\nI2C communication doesn't work properly"
    err_time = 2
    try:
        from smbus import SMBus  # works only on Pi
        bus = SMBus(1)  # indicates /dev/ic2-1 - correct i2c bus for most Pies
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
        import RPi.GPIO as GPIO  # works only on Pi
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(config.gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
        # ensures nothing is being reset during program's start
    except ModuleNotFoundError:
        print("GPIO import - failed")
        sleep(err_time)


def i2c_data():
    sleep_amt = 1
    disable_serial_data = [0]
    on, off = [1], [0]
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