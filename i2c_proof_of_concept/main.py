from flash_common import flash
from time import sleep
import os


def main():
    node1addr = 8
    node2addr = 10
    node3addr = 12
    node4addr = 14
    node5addr = 16
    node6addr = 18
    node7addr = 20
    node8addr = 22

    addr_list_hex = (node1addr, node2addr, node3addr, node4addr,
                     node5addr, node6addr, node7addr, node8addr)

    addr_list = [hex(item) for item in addr_list_hex]

    for addr in addr_list:
        flash(addr)
        print(f"\n\n\t\tNode {str(addr_list.index(addr)+1)} flashed ")
        sleep(2)
        try:
            os.system("i2cdetect -y 1")  # showing currently detected i2c devices
        except PermissionError:
            print("\n\n\tI2C error")


if __name__ == "__main__":
    main()
