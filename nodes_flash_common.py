from time import sleep
import os


def com_init():
    error_msg = "SMBus(1) - error\nI2C communication doesn't work properly"
    err_time = 1
    bus = 0
    try:
        from smbus import SMBus  # works only on Pi
        bus = SMBus(1)  # indicates /dev/ic2-1 - correct i2c bus for most Pies
    except PermissionError as perm_error:
        print(error_msg)
        print(perm_error)
        sleep(err_time)
    except NameError as name_error:
        print(error_msg)
        print(name_error)
        sleep(err_time)
    except ModuleNotFoundError as no_mod_err:
        print(error_msg)
        print(no_mod_err)
        sleep(err_time)
    finally:
        return bus


def gpio_com(config):
    try:
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(config.gpio_reset_pin, GPIO.OUT, initial=GPIO.HIGH)
        # ensures nothing is being reset during program's start
    except ModuleNotFoundError:
        print("GPIO import - failed - works only on Pi")
        sleep(1)


def reset_gpio_pin(config):
    try:
        GPIO = RPi.GPIO()
        GPIO.output(config.gpio_reset_pin, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(config.gpio_reset_pin, GPIO.LOW)
        sleep(0.1)
        GPIO.output(config.gpio_reset_pin, GPIO.HIGH)
        sleep(0.1)
    except AttributeError:
        print("AttributeError - that feature works only on Pi")
        sleep(1)
    except NameError:
        print("AttributeError - that feature works only on Pi")
        sleep(1)


def prepare_mate_node(addr):
    def calculate_checksum(data):
        checksum = sum(data) & 0xFF
        return checksum

    bus = com_init()
    sleep_amt = 1
    on, off = [1], [0]
    reset_mate_node_command = 0x79
    on.append(calculate_checksum(on))
    off.append(calculate_checksum(off))
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on command sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, off)
    print("off command sent")
    sleep(sleep_amt)
    bus.write_i2c_block_data(addr, reset_mate_node_command, on)
    print("on command sent")
    sleep(0.2)


def flash_mate_node(config, firmware_version):
    avrdude_action = f"avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U \
    flash:w:/home/{config.user}/RH-ota/firmware/{firmware_version}.hex:i"
    os.system(f"{avrdude_action}")


def main():
    print("Use file nodes_flash.py as a opening file instead")


if __name__ == "__main__":
    main()
