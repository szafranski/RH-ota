from smbus import SMBus  # works only on Pi
from time import sleep
import os

bus = SMBus(1)  # indicates /dev/ic2-1
addr = 0x0a
x = 1
y = 79
on = 1
off = 0


sleep(1)
bus.write_byte_data(addr, y, on)
bus.write_byte_data(addr, y, on)
print("on sent")
sleep(x)
#long write_byte_data_data(addr,y,1)
bus.write_byte_data(addr, y, off)
bus.write_byte_data(addr, y, off)
print("off sent")
sleep(x)
bus.write_byte_data(addr, y, on)
bus.write_byte_data(addr, y, on)
print("on sent")
sleep(0.5)

os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i")
