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


def flash_blink(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i")


def flash_firmware(config):
    os.system(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i")


def flash_firmware_onto_all_nodes(config):  # nodes have to be 'auto-numbered'
    nodes_num = config.nodes_number
    odd_number = odd_number_of_nodes_check(config)
    addresses = nodes_addresses()
    for i in range(0, nodes_num):
        addr = addresses[i]
        print(f"\n\t\t{Bcolors.BOLD}Flashing node {i + 1} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
        prepare_mate_node(addr) if not config.debug_mode else print("debug mode")
        print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
              f"flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i ")
        flash_firmware(config) if not config.debug_mode else None
        print(f"\n\t\t\t{Bcolors.BOLD}Node {i + 1} - flashed{Bcolors.ENDC}\n\n")
        sleep(2)
        if odd_number and ((nodes_num - i) == 2):  # breaks the "flashing loop" after last even node
            break
    flash_firmware_onto_gpio_node(config) if odd_number else None
    logo_update(config)
    input("\nDone. Press ENTER to continue. ")
    sleep(1)


def flash_firmware_on_a_specific_node(config, selected_node_number):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("debug mode")
    print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i ")
    flash_firmware(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - flashed{Bcolors.ENDC}\n\n")
    sleep(2)


def flash_blink_on_a_specific_node(config, selected_node_number):
    addr = nodes_addresses()[selected_node_number - 1]
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {selected_node_number} {Bcolors.ENDC}(reset with I2C address: {addr})\n")
    prepare_mate_node(addr) if not config.debug_mode else print("debug mode")
    print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
    flash_blink(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {selected_node_number} - flashed{Bcolors.ENDC}\n\n")
    sleep(2)


def flash_firmware_onto_gpio_node(config):
    rst = config.gpio_reset_pin
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {config.nodes_number} {Bcolors.ENDC}(reset with GPIO pin: {rst})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i ")
    flash_blink(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {config.nodes_number} - flashed{Bcolors.ENDC}\n\n")
    sleep(2)


def flash_blink_onto_gpio_node(config):
    rst = config.gpio_reset_pin
    x = int(config.nodes_number)
    print(f"\n\t\t{Bcolors.BOLD}Flashing node {x} {Bcolors.ENDC}(reset with GPIO pin: {rst})\n")
    reset_gpio_pin(config.gpio_reset_pin)
    print(f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
          f"flash:w:/home/{config.user}/RH-ota/firmware/blink.hex:i ")
    flash_blink(config) if not config.debug_mode else None
    print(f"\n\t\t\t{Bcolors.BOLD}Node {x} - flashed{Bcolors.ENDC}\n\n")
    sleep(2)


def node_selection_menu(config):
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
                            
                    {yellow}'e'- Exit to main menu{endc}
                    
        """.format(bold=Bcolors.BOLD, red=Bcolors.RED, yellow=Bcolors.YELLOW, endc=Bcolors.ENDC)
        print(flash_node_menu)
        selection = input(f"\t\t{Bcolors.BOLD}Which node do you want to program: {Bcolors.ENDC}")
        if selection.isdigit():
            if odd_number_of_nodes_check(config):
                if int(selection) in range(config.nodes_number+1) and int(selection) != config.nodes_number:
                    selected_node_number = selection
                    specific_node_menu(config, int(selected_node_number))
                elif int(selection) in range(config.nodes_number+1) and int(selection) == config.nodes_number:
                    odd_node_menu(config)
                elif int(selection) in range(8) and int(selection) not in range(config.nodes_number):
                    print("\n\n\tNode number higher than configured amount of nodes.")
                    sleep(1.5)
            if not odd_number_of_nodes_check(config):
                if int(selection) in range(config.nodes_number+1):
                    selected_node_number = selection
                    specific_node_menu(config, int(selected_node_number))
                elif int(selection) in range(8) and int(selection) not in range(config.nodes_number):
                    print("\n\n\tNode number higher than configured amount of nodes.")
                    sleep(1.5)
        elif selection == 'e':
            break


def specific_node_menu(config, selected_node_number):
    clear_the_screen()
    logo_top(config.debug_mode)
    sleep(0.05)
    while True:
        print(f"""
        {Bcolors.BOLD}\n\n\t\t\tNode {str(selected_node_number)}  selected{Bcolors.ENDC}\n
                Choose flashing type:\n{Bcolors.ENDC}
        1 - {Bcolors.GREEN}Node ground-auto selection firmware - recommended{Bcolors.ENDC}{Bcolors.BOLD}

        2 - Flashes 'blink' on the node - only for test purposes

        a - Abort{Bcolors.ENDC}""")
        selection = input()
        if selection == '1':
            flash_firmware_on_a_specific_node(config, selected_node_number)
            break
        if selection == '2':
            flash_blink_on_a_specific_node(config, selected_node_number)
            break
        if selection == 'a':
            break


def odd_node_menu(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    sleep(0.05)
    odd_number = odd_number_of_nodes_check(config)
    while odd_number:
        print(f"""{Bcolors.BOLD}

                Node {str(config.nodes_number)}  selected{Bcolors.ENDC}

                Choose flashing type:{Bcolors.ENDC}

        1 - {Bcolors.GREEN}Flash firmware on the node - recommended{Bcolors.ENDC}{Bcolors.BOLD}

        2 - Flashes 'blink' on the node - only for test purposes

        a - Abort{Bcolors.ENDC}""")
        selection = input()
        if selection == '1':
            flash_firmware_onto_gpio_node(config)
            return
        if selection == '2':
            flash_blink_onto_gpio_node(config)
            return
        if selection == 'a':
            break
    else:
        clear_the_screen()
        logo_top(config.debug_mode)
        print("\n\n\t\tEven number of nodes detected\n\n")


def first_flashing(config):
    clear_the_screen()
    logo_top(config.debug_mode)

    def flash(port):
        uart_flashing_prompt = f"\n\n\t{Bcolors.BOLD}Hit 'Enter' and push reset key on next node after 1 second " \
                               f"[e - exit] {Bcolors.ENDC}"
        usb_flashing_prompt = f"\n\n\t{Bcolors.BOLD}Connect next Arduino and hit 'Enter' [e - exit] {Bcolors.ENDC}"
        flashing_prompt = 0
        if port == 'USB0':
            flashing_prompt = usb_flashing_prompt
        elif port == 'S0':
            flashing_prompt = uart_flashing_prompt
        while True:
            selection = input(flashing_prompt)
            if selection == 'e':
                break
            else:
                sleep(0.5)
                error = "echo !!! ---- Flashing error - try again ---- !!!"  # todo new line before and after '!!!'
                os.system(f"timeout 10 avrdude -v -p atmega328p -c arduino -P /dev/tty{port} -b 57600 -U \
                        flash:w:/home/{config.user}/RH-ota/firmware/{config.RH_version}/node_0.hex:i || {error}")

    while True:
        first_flash_select = f"""
        {Bcolors.BOLD}
        After selecting right port you will be asked to manually push
        reset button on each node according to instructions on the screen.
        
        Number of iterations of this procedure will correspond to the number
        of nodes declared during the configuration process.  
          
        Will you flash your nodes for the first time via UART (on PCB) 
        or using USB* port? [default: UART]

        1 - UART

        2 - USB 
        
        a - abort{Bcolors.ENDC} 
        
        
        *USB can be used only if node is only device connected to the Pi """
        port_sel = input(first_flash_select)
        if port_sel == '1':
            port_sel = 'S0'
            flash(port_sel)
            break
        if port_sel == '2':
            port_sel = 'USB0'
            flash(port_sel)
            break
        if port_sel == 'a':
            break
        else:
            print("\n\tType: 'UART' or 'USB'\n\t")
    print(f"\n\n\t\t\t{Bcolors.BOLD}FIRMWARE FLASHING - DONE{Bcolors.ENDC}\n\n")
    sleep(2)


def show_i2c_devices(config):
    clear_the_screen()
    logo_top(config.debug_mode)
    print("\n\n")
    os.system("i2cdetect -y 1")
    print("\n\n\tPress Enter to exit to menu\n")


def connection_test(nodes_num):  # todo finish this or remove
    for i in range(nodes_num):
        os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
        sleep(0.2)


def flashing_menu(config):
    while True:
        clear_the_screen()
        logo_top(config.debug_mode)
        sleep(0.05)
        node_menu = """\n\n
                            {bold}{underline}CHOOSE FLASHING TYPE:{endc}
    
                    {green}{bold}1 - Flash each node automatically - rec.{endc}{bold}
    
                    2 - Flash nodes individually
    
                    3 - First time flashing
    
                    4 - Show I2C connected devices
            
                    {yellow}e - Exit to main menu{endc}\n
            """.format(bold=Bcolors.BOLD, green=Bcolors.GREEN, yellow=Bcolors.YELLOW,
                       endc=Bcolors.ENDC, underline=Bcolors.UNDERLINE)
        print(node_menu)
        sleep(0.1)
        selection = input("")
        if selection == '1':
            clear_the_screen()
            flash_firmware_onto_all_nodes(config)
        if selection == '2':
            node_selection_menu(config)
        if selection == '3':
            first_flashing(config)
        if selection == '4':
            show_i2c_devices(config)
        if selection == 'e':
            break


def main():
    config = load_config()
    com_init()
    flashing_menu(config)


if __name__ == "__main__":
    main()
