from flash_common import flash
from time import sleep
import os

nodes_number = 4


def main():
    node1addr = 0x08
    node2addr = 0x0a
    node3addr = 0x0c
    node4addr = 0x0e
    node5addr = 0x10
    node6addr = 0x12
    node7addr = 0x14
    node8addr = 0x16

    addr_list = [node1addr, node2addr, node3addr, node4addr,
                 node5addr, node6addr, node7addr, node8addr]
    i = 0

    for addr in addr_list:

        if i == nodes_number:
            break

        i += 1

        flash(addr)
        print(f"\n\n\t\tNode {str(addr_list.index(addr) + 1)} flashed ")
        sleep(2)
        try:
            os.system("i2cdetect -y 1")  # showing currently detected i2c devices
        except PermissionError:
            print("\n\n\tI2C error")


if __name__ == "__main__":
    main()
