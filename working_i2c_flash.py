from smbus import SMBus  # works only on Pi
from time import sleep
import os

bus = SMBus(1)  # indicates /dev/ic2-1
addr = 0x0a

sleepAmt = 1

reset_mate_node = 0x79
disable_serial_on_the_node = 0x80


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return checksum


on = [1]
off = [0]


def disable_serial():
    sleep(sleepAmt)
    # bus.write_byte(addr, disable_serial_on_the_node)
    bus.write_i2c_block_data(addr, disable_serial_on_the_node, on)
    # which is correct?
    print("serial disabled")
    sleep(sleepAmt)


def flash_mate_node():
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("on sent")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, off)
    print("off sent")
    sleep(sleepAmt)
    bus.write_i2c_block_data(addr, reset_mate_node, on)
    print("on sent")
    sleep(0.2)

    os.system(
        "avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i")


def main():
    disable_serial()
    flash_mate_node()


main()
