from smbus import SMBus  # works only on Pi
from time import sleep
import os

bus = SMBus(1)  # indicates /dev/ic2-1
addr = 0x0a
delay_time = 1
y = 0x79
on = 1
off = 0


sleep(delay_time)
bus.write_byte_data(addr, y, on)
bus.write_byte_data(addr, y, on)
print("on sent")
sleep(delay_time)
bus.write_byte_data(addr, y, off)
bus.write_byte_data(addr, y, off)
print("off sent")
sleep(delay_time)
bus.write_byte_data(addr, y, on)
bus.write_byte_data(addr, y, on)
print("on sent")
sleep(0.5)

sel = input("Flash? y/n")
if sel == 'y':
    os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U "
              "flash:w:/home/pi/RH-ota/firmware/blink.hex:i")
