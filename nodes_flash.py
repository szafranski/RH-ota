from time import sleep
import os
from nodes_flash_common import com_init, gpio_com, prepare_mate_node
from modules import clear_the_screen, Bcolors, logo_top, load_config
from nodes_update_old import main as old_flash_gpio


def nodes_addresses():
    """nodes I2C addresses - below: conversion to hex numbers required by SMBus module"""
    #  node    addr
    node1addr = 0x08
    node2addr = 0x0a
    node3addr = 0x0c
    node4addr = 0x0e
    node5addr = 0x10
    node6addr = 0x12
    node7addr = 0x14
    node8addr = 0x16

# addresses are swapped in the list due to "paired" nature of resetting before flashing
# sending a command to first element on the list causes second node to be flashed etc.

    addr_list_int = [node2addr, node1addr, node4addr, node3addr,
                     node6addr, node5addr, node8addr, node7addr]

    addr_list_str = [str(item) for item in addr_list_int]

    return addr_list_str, addr_list_int


def flash_blink(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i")


def flash_firmware(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i")


def logo_update(config):
    print("""
    #######################################################################
    #                                                                     #
    # {bg}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s} #
    #                                                                     #
    #              {bold}         Thank you!        {endc}                #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=int(config.nodes_number), bold=Bcolors.BOLD_S,
               bg=Bcolors.BOLD_S+Bcolors.GREEN, endc=Bcolors.ENDC_S, s=(9 * ' ')))


def reset_gpio_pin(config):
    GPIO = gpio_com(config)
    GPIO.output(config.gpio_reset_pin, GPIO.LOW)
    sleep(0.1)
    GPIO.output(config.gpio_reset_pin, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(config.gpio_reset_pin, GPIO.LOW)
    sleep(0.1)


def flash_firmware_onto_all_nodes(config):  # nodes have to be 'auto-numbered'
    for i in range(0, int(config.nodes_number)):
        addr = nodes_addresses()[1][i]
        print(f"\n\t\t\t{Bcolors.BOLD}Flashing node {i + 1} (reset with I2C address: {addr}){Bcolors.ENDC}\n")
        if not config.debug_mode:
            prepare_mate_node(addr)
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i ")
        if not config.debug_mode:
            os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/{config.user}"
                      f"/RH-ota/firmware/{config.RH_version}/node_0.hex:i")
        print(f"\n\t\t\t{Bcolors.BOLD}Node {i + 1} - flashed{Bcolors.ENDC}\n\n")
        sleep(2)
    logo_update(config)
    sleep(2)


def flash_nodes_individually(config):
    def node_selection_menu():
        while True:
            clear_the_screen()
            logo_top(config.debug_mode)
            sleep(0.05)
            flash_node_menu = """
            
                                {red}{bold}NODES MENU{endc}
                            {bold}
                    1 - Flash node 1        5 - Flash node 5
    
                    2 - Flash node 2        6 - Flash node 6
    
                    3 - Flash node 3        7 - Flash node 7
    
                    4 - Flash node 4        8 - Flash node 8
                            {yellow}
                          'e'- Exit to main menu{endc}
                        
            """.format(bold=Bcolors.BOLD, red=Bcolors.RED, yellow=Bcolors.YELLOW, endc=Bcolors.ENDC)
            print(flash_node_menu)
            selection = input("""
                    {bold}Which node do you want to program:{endc} """.format(bold=Bcolors.BOLD, endc=Bcolors.ENDC))
            if selection.isdigit():
                if int(selection) in range(int(config.nodes_number)+1):
                    selected_node_number = selection
                    specific_node_menu(int(selected_node_number))
                elif int(selection) in range(8) and int(selection) not in range(int(config.nodes_number)):
                    print("\n\n\tNode number higher than configured amount of nodes.")
                    sleep(1.5)
            elif selection == 'e':
                break
            else:
                continue

    def specific_node_menu(selected_node_number):
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        while True:
            print(f"""
            {Bcolors.BOLD}\n\t\t\tNode {str(selected_node_number)}  selected{Bcolors.ENDC}\n
                    Choose flashing type:\n{Bcolors.ENDC}
            1 - {Bcolors.GREEN}Node ground-auto selection firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}

            2 - Flashes 'Blink' on the node - only for test purposes

            a - Abort{Bcolors.ENDC}""")
            selection = input()
            if selection == '1':
                addr = nodes_addresses()[1][selected_node_number-1]
                x = selected_node_number
                print(f"\n\t\t\t{Bcolors.BOLD}Flashing node {x} (reset with I2C address: {addr}){Bcolors.ENDC}\n")
                if not config.debug_mode:
                    prepare_mate_node(addr)
                print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
                      f"flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i ")
                if not config.debug_mode:
                    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                              f"{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i")
                print(f"\n\t\t\t{Bcolors.BOLD}Node {x} - flashed{Bcolors.ENDC}\n\n")
                sleep(2)
                return
            if selection == '2':
                addr = nodes_addresses()[1][selected_node_number-1]
                x = selected_node_number
                print(f"\n\t\t\t{Bcolors.BOLD}Flashing node {x} (reset with I2C address: {addr}){Bcolors.ENDC}\n")
                if not config.debug_mode:
                    prepare_mate_node(addr)
                print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
                      f"flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
                if not config.debug_mode:
                    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"
                              f"{config.user}/RH-ota/firmware/blink.hex:i")
                print(f"\n\t\t\t{Bcolors.BOLD}Node {x} - flashed{Bcolors.ENDC}\n\n")
                return
            if selection == 'a':
                break
            else:
                continue

    node_selection_menu()


def first_flashing(config):
    clear_the_screen()
    logo_top(config.debug_mode)

    def flash(port):
        for i in range(int(config.nodes_number)):
            selection = input("\n\n\tHit 'Enter' and push reset key of next node after 1 second [a - abort] ")
            if selection == 'a':
                break
            else:
                sleep(0.5)
                os.system(f"sudo avrdude -v -p atmega328p -c arduino -P /dev/tty{port} -b 57600 -U \
                        flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i")

    while True:
        first_flash_select = """\n\n
        Will you flash your nodes for the first time via UART (on PCB) 
        or using USB port? [default: UART]

        1 - UART

        2 - USB \n"""
        port_sel = input(first_flash_select)
        if port_sel == '1':
            port_sel = 'S0'
            flash(port_sel)
            break
        if port_sel == '2':
            port_sel = 'USB0'
            flash(port_sel)
            break
        else:
            print("\n\tType: 'UART' or 'USB'\n\t")
    print(f"\n\t{Bcolors.BOLD}FIRMWARE FLASHING - DONE{Bcolors.ENDC}\n")
    sleep(2)


def show_i2c_devices(config):
    logo_top(config.debug_mode)
    print("\n\n")
    os.system("i2cdetect -y 1")
    input("\n\n\tHit any key when done.")


def connection_test(nodes_num):
    for i in range(nodes_num):
        os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
        sleep(0.2)


def flashing_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        node_menu = """\n
                            {bold}{underline}CHOOSE FLASHING TYPE:{endc}
    
                    {green}{bold}1 - Flash each node automatically - rec.{endc}{bold}
    
                    2 - Flash each node individually
    
                    3 - Flash first time
    
                    4 - Show I2C connected devices
    
                    5 - Flash using GPIO reset pins - obsolete
        
                    {yellow}e - Exit to main menu{endc}
            """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                       endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
        print(node_menu)
        sleep(0.1)
        selection = input()
        if selection == '1':
            flash_firmware_onto_all_nodes(config)
        if selection == '2':
            flash_nodes_individually(config)
        if selection == '3':
            first_flashing(config)
        if selection == '4':
            show_i2c_devices(config)
        if selection == '5':
            old_flash_gpio()
        if selection == 'e':
            break
        else:
            continue


def main():
    config = load_config()
    com_init()
    flashing_menu(config)


if __name__ == "__main__":
    main()
