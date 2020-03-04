from smbus import SMBus
from time import sleep
import os
import sys
import json

if os.path.exists("./updater-config.json") == True:
	with open('updater-config.json') as config_file:
		data = json.load(config_file)
else:
	with open('distr-updater-config.json') as config_file:
		data = json.load(config_file)

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']
preffered_RH_version = data['RH_version']

if preffered_RH_version == 'master':
	firmware_version = 'master'
if preffered_RH_version == 'beta':
	firmware_version = 'beta'
if preffered_RH_version == 'stable':
	firmware_version = 'stable'
if preffered_RH_version == 'custom':
	firmware_version = 'stable'

addr = 0x08 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

def main():
	selection=str(raw_input("What do you want to send?"))
	if selection=='1':
		bus.write_byte(addr, 0x1) # switch it on
	if selection=='0':
		bus.write_byte(addr, 0x0) # switch it on
	if selection=='2':
		bus.write_byte(addr, 0x0) # switch it on
		sleep(0.5)
		bus.write_byte(addr, 0x1) # switch it on
		os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
		print("\n\t Node 1 flashed\n")
		sleep(1.5)
	main()
main()

