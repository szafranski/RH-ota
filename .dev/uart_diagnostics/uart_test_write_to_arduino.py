import serial


# serial_port_name = "ttyS0"


def serial_test_write(serial_port_name):
    my_serial = serial.Serial(f'/dev/{serial_port_name}', 9600)

    print(f"""
    Writing to {serial_port_name} for 10 seconds - check Arduino's built-in LED
    
    Watch for 2 short, one long. If present - {serial_port_name} is your Serial port.
    """)
    for _ in range(3):
        my_serial.write(1)


def custom_port_selection():
    serial_port_name = input("Please enter custom UART port name or exit? like: 'ttyS0':\t").replace(" ", "")
    serial_test_write(serial_port_name)
    while True:
        selection = input("Would you like to enter another port name? | [y/n]\t").lower()
        if selection == "n":
            break
        elif selection == "y":
            serial_port_name = input("\nEnter port name you'd like to try:\t\t").replace(" ", "")
            serial_test_write(serial_port_name)


def main():
    custom_port_selection()


if __name__ == "__main__":
    main()
