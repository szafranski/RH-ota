from time import sleep
import os
from nodes_flash_common import com_init, prepare_mate_node, reset_gpio_pin
from modules import clear_the_screen, Bcolors, logo_top, load_config


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


def firmware_version_selection(config):
    if config.rh_version in ['stable', 'beta']:
        firmware_version = config.rh_version
    elif config.rh_version in ['master', 'main']:
        firmware_version = 'main'
    else:  # in case of 'custom' RH version - firmware defaults to 'stable'
        firmware_version = 'stable'

    return firmware_version


def logo_update(config):
    print("""
    #######################################################################
    #                                                                     #
    # {bg}{s}Flashing firmware onto {nodes_number} nodes - DONE{endc}{s} #
    #                                                                     #
    #              {bold}         Thank you!        {endc}                #
    #                                                                     #
    #######################################################################\n\n
    """.format(nodes_number=config.nodes_number, bold=Bcolors.BOLD_S,
               bg=Bcolors.BOLD_S + Bcolors.GREEN, endc=Bcolors.ENDC_S, s=(9 * ' ')))


def odd_number_of_nodes_check(config):
    nodes_number = config.nodes_number
    odd_nodes_flag = True if nodes_number % 2 != 0 else False
    return odd_nodes_flag


def show_flashing_error_msg():
    flashing_error_msg = f'printf "\n\n{Bcolors.RED}    !!! ---- Flashing error - both bootloaders - try again ---- !!! ' \
                  f'{Bcolors.ENDC}\n\n"'
    return flashing_error_msg


def old_bootloader_flashing_error_handler(config):
    old_boot_flashing_error = f'(printf "\n\n{Bcolors.YELLOW}      Flashing error - trying with new bootloader  {Bcolors.ENDC}\n\n" \
                  && touch /home/{config.user}/RH-ota/.flashing_error) && sleep 1'
    return old_boot_flashing_error


def show_uart_con_error_msg():
    uart_error = f'printf "\n\n{Bcolors.RED}    !!! ---- No UART connection with a device ---- !!! {Bcolors.ENDC}\n\n"'
    return uart_error


def flash_blink_onto_a_node(config, bootloader_version=0):
    if bootloader_version == 0:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i \
    || {old_bootloader_flashing_error_handler(config)}")
    else:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/blink.hex:i \
    || {show_flashing_error_msg()}")


def flash_custom_firmware_onto_a_node(config, bootloader_version=0):
    if bootloader_version == 0:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/custom_firmware/custom_node.hex:i || \
    || {old_bootloader_flashing_error_handler(config)}")
    else:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/custom_firmware/custom_node.hex:i || \
    || {show_flashing_error_msg()}")


def flash_firmware_onto_a_node(config, bootloader_version=0):  # 0 - old bootloader; 1 - new bootloader
    if bootloader_version == 0:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i \
    || {old_bootloader_flashing_error_handler(config)}")
    else:
        os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/{firmware_version_selection(config)}/node_0.hex:i \
    || {show_flashing_error_msg()}")


# below works when nodes are 'auto-numbered'
def flash_firmware_onto_all_nodes(config):
    clear_the_screen()
    print(f"\n\t\t\t{Bcolors.BOLD}Flashing procedure started{Bcolors.BOLD}\n\n")
    nodes_num = config.nodes_number
    odd_number = odd_number_of_nodes_check(config)
    addresses = nodes_addresses()
    if nodes_num == 1:
        flash_firmware_onto_a_gpio_node(config) if odd_number else None
    else:
        for i in range(0, nodes_num):
            addr = addresses[i]
            print(f"\n\t\t{Bcolors.BOLD}Flashing node {i + 1} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
            prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
            print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 "
                  f"-U flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
            flash_firmware_onto_a_node(config, 0) if not config.debug_mode else None
            old_bootloader_flashing_error = os.path.exists(f"/home/{config.user}/RH-ota/.flashing_error")
            if old_bootloader_flashing_error:
                print(
                    f"\n\t\t{Bcolors.BOLD}Flashing node {i + 1} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
                print("new bootloader\n")
                prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
                print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U "
                      f"flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
                flash_firmware_onto_a_node(config, 1) if not config.debug_mode else None
                os.system(f"rm /home/{config.user}/RH-ota/.flashing_error")
            print(f"\n\t\t\t{Bcolors.BOLD}Node {i + 1} - flashed{Bcolors.ENDC}\n\n")
            sleep(2)
            if odd_number and ((nodes_num - i) == 2):
                break  # breaks the "flashing loop" after last even node
        flash_firmware_onto_a_gpio_node(config) if odd_number else None
    logo_update(config)
    input("\nDone. Press ENTER to continue ")
    sleep(1)


# below works when nodes are 'auto-numbered'
def flash_custom_firmware_onto_all_nodes(config, bootloader_version="old_bootloader", flashing_baudrate="57600"):
    clear_the_screen()
    print(f"\n\t\t\t{Bcolors.BOLD}Flashing procedure started{Bcolors.BOLD}\n\n")
    nodes_num = config.nodes_number
    odd_number = odd_number_of_nodes_check(config)
    addresses = nodes_addresses()
    for i in range(0, nodes_num):
        addr = addresses[i]
        print(f"\n\t\t\t{Bcolors.BOLD}Flashing node {i + 1} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate} -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/{bootloader_version}/custom_firmware/custom_node.hex:i")
        flash_custom_firmware_onto_gpio_node(config) if not config.debug_mode else None
        print(f"\n\t\t\t{Bcolors.BOLD}Node {i + 1} - flashed{Bcolors.ENDC}\n\n")
        sleep(2)
        if odd_number and ((nodes_num - i) == 2):
            break  # breaks the "flashing loop" after last even node
    flash_custom_firmware_onto_gpio_node(config) if odd_number else None
    logo_update(config)
    input("\nPress ENTER to continue")
    sleep(2)


def flash_firmware_on_a_specific_node(config, selected_node_number):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
    flash_firmware_onto_a_node(config, 0) if not config.debug_mode else None
    old_bootloader_flashing_error = os.path.exists(f"/home/{config.user}/RH-ota/.flashing_error")
    if old_bootloader_flashing_error:
        print(
            f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        print("new bootloader\n")
        prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
        flash_firmware_onto_a_node(config, 1) if not config.debug_mode else None
        os.system(f"rm /home/{config.user}/RH-ota/.flashing_error")
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def flash_firmware_onto_a_gpio_node(config):
    reset_pin = config.gpio_reset_pin
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {config.nodes_number} {Bcolors.ENDC}(reset with GPIO pin: {reset_pin})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
    flash_firmware_onto_a_node(config, 0) if not config.debug_mode else None
    old_bootloader_flashing_error = os.path.exists(f"/home/{config.user}/RH-ota/.flashing_error")
    if old_bootloader_flashing_error:
        print(
            f"\n\t\t{Bcolors.BOLD}Flashing node {config.nodes_number} {Bcolors.ENDC}(reset with GPIO pin: {reset_pin})\n")
        print("new bootloader\n")
        reset_gpio_pin(config.gpio_reset_pin)
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/{firmware_version_selection(config)}/node_0.hex:i")
        flash_firmware_onto_a_node(config, 1) if not config.debug_mode else None
        os.system(f"rm /home/{config.user}/RH-ota/.flashing_error")
    print(f"\n\t\t\t{Bcolors.BOLD}Node {config.nodes_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def flash_custom_firmware_on_a_specific_node(config, selected_node_number):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/custom_firmware/custom_node.hex:i ")
    flash_custom_firmware_onto_a_node(config, 0) if not config.debug_mode else None
    old_bootloader_flashing_error = os.path.exists(f"/home/{config.user}/RH-ota/.flashing_error")
    if old_bootloader_flashing_error:
        print(
            f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        print("trying with new bootloader")
        prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/custom_firmware/custom_node.hex:i ")
        flash_custom_firmware_onto_a_node(config, 1) if not config.debug_mode else None
        os.system(f"rm /home/{config.user}/RH-ota/.flashing_error")
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def flash_blink_on_a_specific_node(config, selected_node_number):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/blink.hex:i ")
    flash_blink_onto_a_node(config, 0) if not config.debug_mode else None
    old_bootloader_flashing_error = os.path.exists(f"/home/{config.user}/RH-ota/.flashing_error")
    if old_bootloader_flashing_error:
        print(
            f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        print("trying with new bootloader")
        prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 115200 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/blink.hex:i")
        flash_blink_onto_a_node(config, 1) if not config.debug_mode else None
        os.system(f"rm /home/{config.user}/RH-ota/.flashing_error")
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def flash_custom_firmware_onto_gpio_node(config):
    reset_pin = config.gpio_reset_pin
    x = int(config.nodes_number)
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {x} {Bcolors.ENDC}(reset with GPIO pin: {reset_pin})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/custom_firmware/custom_node.hex:i ")
    flash_custom_firmware_onto_a_node(config, 0) if not config.debug_mode else None

    print(f"\n\t\t\t{Bcolors.BOLD}Node {x} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def flash_blink_onto_gpio_node(config, bootloader_version="old_bootloader", flashing_baudrate="57600"):
    reset_pin = config.gpio_reset_pin
    x = int(config.nodes_number)
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {x} {Bcolors.ENDC}(reset with GPIO pin: {reset_pin})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate} -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/{bootloader_version}/blink.hex:i ")
    flash_blink_onto_a_node(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {x} - flashed{Bcolors.ENDC}\n\n")
    input("\nPress ENTER to continue")
    sleep(2)


def node_selection_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        flash_node_menu = """\n

                    {red}{bold}NODES MENU{endc}{bold}

                1 - Flash node 1        5 - Flash node 5

                2 - Flash node 2        6 - Flash node 6

                3 - Flash node 3        7 - Flash node 7

                4 - Flash node 4        8 - Flash node 8 

                   {yellow}e - Exit to main menu{endc}

        """.format(bold=Bcolors.BOLD_S, red=Bcolors.RED_S, yellow=Bcolors.YELLOW_S, endc=Bcolors.ENDC)
        print(flash_node_menu)
        selection = input(f"\t\t{Bcolors.BOLD}Which node do you want to program: {Bcolors.ENDC}")
        if selection.isdigit():
            if odd_number_of_nodes_check(config):
                if int(selection) in range(config.nodes_number + 1) and int(selection) != config.nodes_number:
                    selected_node_number = selection
                    specific_node_menu(config, int(selected_node_number))
                elif int(selection) in range(config.nodes_number + 1) and int(selection) == config.nodes_number:
                    odd_node_menu(config)
                elif int(selection) in range(8) and int(selection) not in range(config.nodes_number):
                    print("\n\n\tNode number higher than configured amount of nodes.")
                    sleep(1.5)
            elif not odd_number_of_nodes_check(config):
                if int(selection) in range(config.nodes_number + 1):
                    selected_node_number = selection
                    specific_node_menu(config, int(selected_node_number))
                elif int(selection) in range(8) and int(selection) not in range(config.nodes_number):
                    print("\n\n\tNode number higher than configured amount of nodes.")
                    sleep(1.5)
        elif selection == 'e':
            break


def specific_node_menu(config, selected_node_number):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        node_selected_menu = f"""
        {Bcolors.BOLD}\n\t\t\tNode {str(selected_node_number)}  selected{Bcolors.ENDC}\n
                Choose flashing type:\n{Bcolors.ENDC}
        1 - {Bcolors.GREEN}Node ground-auto selection firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}

        2 - Flash custom firmware on the node

        3 - Flash 'blink' on the node - only for test purposes

        4 - Check UART connection with a node

        e - Exit{Bcolors.ENDC}"""
        print(node_selected_menu)
        selection = input()
        if selection == '1':
            flash_firmware_on_a_specific_node(config, selected_node_number)
        elif selection == '2':
            flash_custom_firmware_on_a_specific_node(config, selected_node_number)
        elif selection == '3':
            flash_blink_on_a_specific_node(config, selected_node_number)
        elif selection == '4':
            check_uart_con_with_a_node(config, selected_node_number)
        elif selection == 'e':
            break
        else:
            continue
        break


def odd_node_menu(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    odd_number = odd_number_of_nodes_check(config)
    while odd_number:
        print(f"""{Bcolors.BOLD}

                Node {str(config.nodes_number)}  selected{Bcolors.ENDC}

                Choose flashing type:{Bcolors.ENDC}

        1 - {Bcolors.GREEN}Flash firmware on the node - recommended{Bcolors.ENDC}{Bcolors.BOLD}

        2 - Flash custom firmware on the node

        3 - Flash 'blink' on the node - only for test purposes

        e - Exit{Bcolors.ENDC}""")
        selection = input()
        if selection == '1':
            flash_firmware_onto_a_gpio_node(config)
            return
        elif selection == '2':
            flash_custom_firmware_onto_gpio_node(config)
            break
        elif selection == '3':
            print("""
            Remember to flash firmware back on the node - later. 
            Only one of the paired nodes can be flashed with 'blink'
            """)
            input("Hit Enter")
            flash_blink_onto_gpio_node(config)
            return
        elif selection == 'e':
            break
    else:
        clear_the_screen()
        logo_top(config.debug_mode)
        print("\n\n\t\tEven number of nodes detected\n\n")


def first_flashing(config):
    clear_the_screen()
    logo_top(config.debug_mode)

    def flash_node_first_time(port):
        first_attempt = f"timeout 20 avrdude -v -p atmega328p -c arduino -P /dev/{port} -b 57600 -U \
        flash:w:/home/{config.user}/RH-ota/firmware/old_bootloader/{firmware_version_selection(config)}/node_0.hex:i"
        first_attempt_error_msg = f'printf "\n\n{Bcolors.YELLOW}Unsuccessful flashing - trying with new bootloader {Bcolors.ENDC}\n\n"'
        second_attempt = f"sleep 3 && timeout 20 avrdude -v -p atmega328p -c arduino -P /dev/{port} -b 115200 -U \
        flash:w:/home/{config.user}/RH-ota/firmware/new_bootloader/{firmware_version_selection(config)}/node_0.hex:i"
        uart_flashing_prompt = \
            "\n\n\t{bg}Hit 'Enter' and push reset button on next node after a second {e}{br}[e - exit] {e}" \
            "".format(br=Bcolors.RED + Bcolors.BOLD, bg=Bcolors.GREEN + Bcolors.BOLD, e=Bcolors.ENDC)
        usb_flashing_prompt = \
            "\n\n\t{bg}Connect next Arduino and hit 'Enter'{e} {br}[e - exit] {e}" \
            "".format(br=Bcolors.RED + Bcolors.BOLD, bg=Bcolors.GREEN + Bcolors.BOLD, e=Bcolors.ENDC)
        flashing_prompt = 0
        if port == 'ttyUSB0':
            flashing_prompt = usb_flashing_prompt
        else:
            flashing_prompt = uart_flashing_prompt
        while True:
            selection = input(flashing_prompt)
            if selection == 'e':
                break
            else:
                sleep(0.5)
                os.system(f"""{first_attempt} || ({first_attempt_error_msg} && {second_attempt}) || {show_flashing_error_msg()}""")

    while True:
        first_flash_select = """
        {bold}
        After selecting right port you will be asked to manually push
        reset button on each node according to instructions on the screen.

        After flashing last node for the first time hit 'e' to exit.

        Will you flash your nodes for the first time via UART (on PCB) 
        or using USB* port? [default: UART]

     {green}1 - UART (port ttyS0 - default){endc}{bold}

            2 - UART (port ttyAMA0 - try in case of errors)

            3 - USB (node connected to Pi's USB port)

            4 - Custom port selection

    {yellow}e - Exit{endc} 


""".format(green=Bcolors.GREEN_S, yellow=Bcolors.YELLOW_S, bold=Bcolors.BOLD, endc=Bcolors.ENDC)
        port_selection = input(first_flash_select)
        if port_selection == '1':
            flash_node_first_time('ttyS0')
        elif port_selection == '2':
            flash_node_first_time('ttyAMA0')
        elif port_selection == '3':
            usb_msg = """
    You are about to attempt first time firmware flashing via Pi's USB port.
    Node has to be ONLY device connected to Raspberry's USB 
    or connected to port named 'USB0'.
    Note that Arduino has to be DISCONNECTED from the PCB during the operation."""

            print(usb_msg)
            input("\n\tHit Enter when you will be ready ")
            flash_node_first_time('ttyUSB0')
        elif port_selection == '4':
            custom_port_selected = str(input("\n\tEnter custom port name here: "))
            flash_node_first_time(custom_port_selected)
        elif port_selection == 'e':
            break
        else:
            print("\n\tType: 'UART' or 'USB'\n\t")
            continue
        break
    print(f"\n\n\t\t\t{Bcolors.BOLD + Bcolors.UNDERLINE}FIRMWARE FLASHING - DONE{Bcolors.ENDC}\n\n")
    sleep(2)


def show_i2c_devices(config):
    while True:
        clear_the_screen()
        try:
            bus_number = config.i2c_bus_number
        except AttributeError:
            bus_number = 1  # defaulting to "1" cause Raspberry Pi uses it; in case of older json with no i2c_bus key
        detected_i2c_devices = os.popen(f"i2cdetect -y {bus_number}").read()
        print(f"\n\t{Bcolors.BOLD}Devices found on the {Bcolors.UNDERLINE}I2C bus {bus_number}{Bcolors.ENDC}:\n")
        print(Bcolors.BOLD)
        print(detected_i2c_devices)
        print(Bcolors.ENDC)
        # done that way because of the way how python is reading/converting hex numbers
        # and how raspberry is reporting addresses
        # space after an address is needed so line "number" is not being read as an address by mistake
        nodes_found = 0
        print("Nodes detected:")
        # don't change below to 'elif' - each node is a separate instance of "found"
        if '08 ' in detected_i2c_devices:
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
        if '10 ' in detected_i2c_devices:
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

        if nodes_found == 0:
            print(f"{Bcolors.RED}\nNo nodes detected{Bcolors.ENDC}")
        else:
            print(f"\n{Bcolors.GREEN}Detected nodes: {nodes_found}{Bcolors.ENDC}\n\n")

        if '76 ' in detected_i2c_devices or '77 ' in detected_i2c_devices:
            bme_found_flag = True
        else:
            bme_found_flag = False

        possible_ina_addr = ['40 ', '41 ', '43 ', '44 ']
        for item in possible_ina_addr:
            if item in detected_i2c_devices:
                ina_found_flag = True
                break
        else:
            ina_found_flag = False

        if bme_found_flag or ina_found_flag:
            print("\nSensors found: ")
            if bme_found_flag:
                print(f"{Bcolors.GREEN}BME sensor 280 found{Bcolors.ENDC}")
            if ina_found_flag:
                print(f"{Bcolors.GREEN}INA sensor 219 found{Bcolors.ENDC}")
        else:
            print("No additional sensors found")

        possible_rtc_addr = ['68 ', 'UU ', '50 ', '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ']
        for item in possible_rtc_addr:
            if item in detected_i2c_devices:
                rtc_found_flag = True
                break
        else:
            rtc_found_flag = False

        if rtc_found_flag:
            print(f"{Bcolors.GREEN}\n\nRTC (DS3231 or PCF8523 or DS1307) found{Bcolors.ENDC}")
        else:
            print("\n\nNo RTC found")

        print(Bcolors.ENDC)
        print(f"\n\n\t{Bcolors.RED}Press 'e' to exit to menu {Bcolors.ENDC}or hit 'Enter' to refresh")
        selection = input("\n")
        if selection == 'e':
            break


def check_uart_connection(config, flashing_baudrate="57600"):
    os.system(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate} \
    || {show_uart_con_error_msg()}")


def check_uart_con_with_a_node(config, selected_node_number, flashing_baudrate="57600"):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Checking node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate}")
    check_uart_connection(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - checked{Bcolors.ENDC}\n\n")
    sleep(1)
    input("\nPress ENTER to continue")


def check_uart_con_with_gpio_node(config, flashing_baudrate="57600"):
    reset_pin = config.gpio_reset_pin
    print(f"\n\t\t{Bcolors.BOLD}Checking node {config.nodes_number} {Bcolors.ENDC}(reset with GPIO pin: {reset_pin})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate}")
    check_uart_connection(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {config.nodes_number} - checked{Bcolors.ENDC}\n\n")
    sleep(1)
    input("\nPress ENTER to continue")


# below works when nodes are 'auto-numbered'
def check_uart_devices(config, flashing_baudrate="57600"):
    nodes_num = config.nodes_number
    odd_number = odd_number_of_nodes_check(config)
    addresses = nodes_addresses()
    for i in range(0, nodes_num):
        addr = addresses[i]
        print(f"\n\t\t{Bcolors.BOLD}Checking node {i + 1} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        prepare_mate_node(addr) if not config.debug_mode else print("simulation mode - flashing disabled")
        print(f"timeout 13 avrdude -v -p atmega328p -c arduino -P /dev/{config.port_name} -b {flashing_baudrate}")
        check_uart_connection(config) if not config.debug_mode else None
        print(f"\n\t\t\t{Bcolors.BOLD}Node {i + 1} - checked{Bcolors.ENDC}\n\n")
        sleep(1)
        input("\nPress ENTER to continue\n")
        if odd_number and ((nodes_num - i) == 2):
            break  # breaks the "flashing loop" after last even node
    check_uart_con_with_gpio_node(config) if odd_number else None
    input("\nPress ENTER to continue")
    sleep(1)


def flashing_menu(config):
    while True:
        os.system(f"rm /home/{config.user}/RH-ota/.flashing_error > /dev/null 2>&1")
        clear_the_screen()
        logo_top(config.debug_mode)
        node_menu = """\n

                          {rmh}FLASHING MENU{endc}


       {green}{bold}1 - Flash each node automatically{endc}{bold}

                    2 - Flash nodes individually

                    3 - First time flashing

                    4 - Show I2C connected devices

                    5 - Check connection with nodes

            {yellow}e - Exit to main menu{endc}\n
            """.format(bold=Bcolors.BOLD_S, green=Bcolors.GREEN_S, yellow=Bcolors.YELLOW_S,
                       endc=Bcolors.ENDC, red=Bcolors.RED_S, underline=Bcolors.UNDERLINE_S,
                       rmh=Bcolors.RED_MENU_HEADER)
        print(node_menu)
        sleep(0.1)
        selection = input("")
        if selection == '1':
            flash_firmware_onto_all_nodes(config)
        elif selection == '2':
            node_selection_menu(config)
        elif selection == '3':
            first_flashing(config)
        elif selection == '4':
            show_i2c_devices(config)
        elif selection == '5':
            check_uart_devices(config)
        elif selection == 'custom':
            flash_custom_firmware_onto_all_nodes(config)
        elif selection == 'e':
            break


def main():
    config = load_config()
    com_init(config)
    flashing_menu(config)


if __name__ == "__main__":
    main()
