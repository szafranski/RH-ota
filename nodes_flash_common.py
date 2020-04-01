from time import sleep
import os
from modules import load_config


def com_init():  # I was trying to assume that software could be open on Linux but idk anymore
    error_msg = "SMBus(1) - error\nI2C communication doesn't work properly"
    err_time = 2
    try:
        from smbus import SMBus  # works only on Pi
        bus = SMBus(1)  # indicates /dev/ic2-1 - correct i2c bus for most Pies
    except PermissionError as perm_error:
        print(error_msg)
        print(perm_error)
        sleep(err_time)
        bus = 0
    except NameError as name_error:
        print(error_msg)
        print(name_error)
        sleep(err_time)
        bus = 0
    except ModuleNotFoundError as no_mod_err:
        print(error_msg)
        print(no_mod_err)
        sleep(err_time)
        bus = 0

    try:
        import RPi.GPIO as GPIO # works only on Pi
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(config.gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
        # ensures nothing is being reset during program's start
    except ModuleNotFoundError:
        print("GPIO import - failed")
        sleep(err_time)

    finally:
        return bus


def reset_gpio_pin(config):
    GPIO = RPi.GPIO()
    GPIO.output(config.gpio_reset_pin, GPIO.HIGH)
    sleep(0.1)
    GPIO.output(config.gpio_reset_pin, GPIO.LOW)
    sleep(0.1)
    GPIO.output(config.gpio_reset_pin, GPIO.HIGH)
    sleep(0.1)


def disable_serial_on_the_node(addr, bus):
    def calculate_checksum(data):
        checksum = sum(data) & 0xFF
        return checksum

    sleep_amt = 1
    disable_serial_data = [0]
    disable_serial_on_the_node_command = 0x80
    disable_serial_data.append(calculate_checksum(disable_serial_on_the_node_command))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, disable_serial_on_the_node_command, disable_serial_data)
    sleep(sleep_amt)
    print(f"serial disabled on the node {str(addr)}")
    sleep(sleep_amt)


def prepare_mate_node(addr, bus):
    def calculate_checksum(data):
        checksum = sum(data) & 0xFF
        return checksum

    sleep_amt = 1
    on, off = [1], [0]
    reset_mate_node_command = 0x79
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, off)
    print("off sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on sent")
    sleep(0.2)


def flash_mate_node(firmware):
    avrdude_action = f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/pi/{firmware}.hex:i"
    os.system(f"{avrdude_action}")


def main(addr):
    config = load_config()
    disable_serial_on_the_node(com_init()[0], addr)
    if config.debug_mode:
        com_init()
    prepare_mate_node(com_init()[0], addr)
    flash_mate_node(config.RH_version)


if __name__ == "__main__":
    main()