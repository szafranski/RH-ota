# define pins
# pins low as a function
# define number of pins
# confirmation

#reset_1=?
#reset_2=?
#reset_3=?
#reset_4=?

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
import os
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)


sleep(0.3)
os.system("echo")
os.system("echo")
os.system("echo")
os.system("echo '     ##########################################################################################'")
os.system("echo '     ###                                                                                    ###'")
os.system("echo '     ###                                  RotorHazard                                       ###'")
os.system("echo '     ###                                                                                    ###'")
os.system("echo '     ###  You are about to update nodes firmware. Please do not interrupt this operation!   ###'")
os.system("echo '     ###                                                                                    ###'")
os.system("echo '     ##########################################################################################'")
os.system("echo")
os.system("echo")

##### confirmation   ######


os.system("sudo pkill server.py")
os.system("sudo systemctl stop rotorhazard")
sleep(0.3)

GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
sleep(0.5)
GPIO.output(12, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)
GPIO.output(26, GPIO.HIGH)

sleep(0.3)
os.system("sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:blank.hex:i")


os.system("echo")
os.system("echo '     Node 1 - flashed'")
os.system("echo")
os.system("echo")
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
sleep(0.5)
GPIO.output(12, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)
GPIO.output(26, GPIO.HIGH)


sleep(0.3)
os.system("sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:blank.hex:i")


os.system("echo")
os.system("echo '     Node 2 - flashed'")
os.system("echo")
os.system("echo")
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
sleep(0.5)
GPIO.output(12, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)
GPIO.output(26, GPIO.HIGH)
sleep(0.3)
os.system("sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:blank.hex:i")


os.system("echo")
os.system("echo '     Node 3 - flashed'")
os.system("echo")
os.system("echo")
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(26, GPIO.LOW)
sleep(0.5)
GPIO.output(12, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)
GPIO.output(26, GPIO.HIGH)
sleep(0.3)

os.system("sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
os.system("sudo avrdude -c linuxgpio -p atmega328p -v -U flash:w:blank.hex:i")

os.system("sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")


os.system("echo")
os.system("echo '     Node 4 - flashed'")
os.system("echo")
os.system("echo")
sleep(0.3)
os.system("echo '     ########################################################################################'")
os.system("echo '     ###                                                                                  ###'")
os.system("echo '     ###  CONGRATULATIONS!              Flashing firmware to nodes - DONE                 ###'")
os.system("echo '     ###                                                                                  ###'")
os.system("echo '     ###  Please power off the timer, unplug voltage source  for few seconds and reboot   ###'")
os.system("echo '     ###                                                                                  ###'")
os.system("echo '     ########################################################################################'")
os.system("echo")
os.system("echo")
sleep(2)

