from smbus import SMBus  # works only on Pi
from time import sleep
import os


def flash(addr):
    bus = SMBus(1)  # indicates /dev/ic2-1

    firmware = 'node'

    sleep_amt = 1

    reset_mate_node = 0x79
    disable_serial_on_the_node = 0x80

    flash_before = False

    def calculate_checksum(data):
        checksum = sum(data) & 0xFF
        return checksum

    on = [1]
    off = [0]

    ser = [0]

    def disable_serial(addr):
        ser.append(calculate_checksum(ser))
        sleep(sleep_amt)
        bus.write_i2c_block_data(addr, disable_serial_on_the_node, ser)
        sleep(1)
        print("serial disabled")
        sleep(sleep_amt)

    def flash_mate_node(addr):
        on.append(calculate_checksum(on))
        off.append(calculate_checksum(off))
        sleep(sleep_amt)
        bus.write_i2c_block_data(addr, reset_mate_node, on)
        print("on sent")
        sleep(sleep_amt)
        bus.write_i2c_block_data(addr, reset_mate_node, off)
        print("off sent")
        sleep(sleep_amt)
        bus.write_i2c_block_data(addr, reset_mate_node, on)
        print("on sent")
        sleep(0.2)

    def flash_it(firm):
        avrdude_content = f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
        flash:w:/home/pi/RH-ota/i2c_proof_of_concept/{firm}.hex:i"
        os.system(f"{avrdude_content}")

    if flash_before:
        flash_it(firmware)
        flash_it(firmware)

    disable_serial(addr)
    flash_mate_node(addr)
    flash_it(firmware)
    # sleep(sleep_amt)
    # os.system("i2cdetect -y 1")
    # flash_mate_node(addr2)
    # flash_it(firmware)
