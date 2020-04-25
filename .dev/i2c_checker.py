import os


def nodes_addresses():
    # nodes I2C addresses - below: hex format is required by SMBus module
    # "RH" are address in RotorHazard node firmware code "format" (rhnode file)

    #  node     addr   RH
    node1addr = 0x08  # 8   - 1st node I2C hardware address
    node2addr = 0x0a  # 10  - 2nd node I2C hardware address
    node3addr = 0x0c  # 12  - 3rd node I2C hardware address
    node4addr = 0x0e  # 14  - 4th node I2C hardware address
    node5addr = 0x10  # 16  - 5th node I2C hardware address
    node6addr = 0x12  # 18  - 6th node I2C hardware address
    node7addr = 0x14  # 20  - 7th node I2C hardware address
    node8addr = 0x16  # 22  - 8th node I2C hardware address

    # addresses are swapped in the list due to "paired" nature of resetting before flashing
    # sending a command to first element on the list causes second node to be flashed etc.

    addr_list = [node2addr, node1addr, node4addr, node3addr,
                 node6addr, node5addr, node8addr, node7addr]

    return addr_list

def check_for_i2c_devices():

    detected_i2c_devices = os.popen("i2cdetect -y 1").read()

    print(detected_i2c_devices)

    nodes_found = 0
    if '08 ' in detected_i2c_devices:
        print("Nodes detected:")
        print(f"Node 1 found")
        nodes_found += 1
    if '0a ' in detected_i2c_devices:
        print(f"Node 2 found")
        nodes_found += 1
    if '0c ' in detected_i2c_devices:
        print(f"Node 3 found")
        nodes_found += 1
    if '0e ' in detected_i2c_devices:
        print(f"Node 4 found")
        nodes_found += 1
    if '10 :' in detected_i2c_devices:
        print(f"Node 5 found")
        nodes_found += 1
    if '12 ' in detected_i2c_devices:
        print(f"Node 6 found")
        nodes_found += 1
    if '14 ' in detected_i2c_devices:
        print(f"Node 7 found")
        nodes_found += 1
    if '16 ' in detected_i2c_devices:
        print(f"Node 8 found")
        nodes_found += 1

    if nodes_found > 0:
        print(f"\nDetected nodes: {nodes_found}")
    else:
        print("\nNo nodes detected")


