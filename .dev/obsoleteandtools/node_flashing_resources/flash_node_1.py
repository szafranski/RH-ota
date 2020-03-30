from time import sleep
from flash_common import communication_initializing


def calculate_checksum(data):
    checksum = sum(data) & 0xFF
    return checksum


communication_initializing()


def reset_mate_node(addr):
    sleep_amt = 1
    disable_serial_data = [0]
    on, off = [1], [0]
    reset_mate_node_command = 0x79
    disable_serial_on_the_node_command = 0x80
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
