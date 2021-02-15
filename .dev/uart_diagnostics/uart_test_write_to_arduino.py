import serial


# serial_port_name = "ttyS0"


def serial_test_write(serial_port_name):
    ser = serial.Serial(f'/dev/{serial_port_name}', 9600)

    ser.write(serial_port_name)
    print(f"""
    Writing to ttyS0 for 10 seconds - check Arduino's built-in LED
    
    Watch for 2 short, one long. If present - {serial_port_name} is your Serial port.
    """)


def custom_port_selection():
    selection = input("Would you like to enter custom UART port name or exit? | y/N").lower()
    while True:
        if selection == "n":
            break
        elif selection == "y":
            serial_port_name = input("Enter port name you'd like to try")
            serial_test_write(serial_port_name)
            break
        else:
            print("Please type 'y' or 'n'")
