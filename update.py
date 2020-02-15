# pins low/high as a function
# define number of pins
# flashed - only after success 
###
reset_1 = 12
reset_2 = 13
reset_3 = 16
reset_4 = 26

#import RPi.#GPIO as #GPIO # Import Raspberry Pi #GPIO library
from time import sleep # Import the sleep function from the time module
import os
import sys

#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(#GPIO.BCM) # Use BCM pin numbering
#GPIO.setup(reset_1, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_2, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_3, #GPIO.OUT, initial=#GPIO.HIGH)
#GPIO.setup(reset_4, #GPIO.OUT, initial=#GPIO.HIGH)

#os.system("cls")
os.system("clear")
sleep(0.1)
print("\n\n\n")	
print("			##########################################################################################")
print("			###                                                                                    ###")
print("			###                                 RotorHazard                                        ###")
print("			###                                                                                    ###")
print("			###    You are about to update nodes firmware. Please do not interrupt this operation! ###")
print("			###                                                                                    ###")
print("			###                                                                                    ###")
print("			##########################################################################################")
print("\n\n\n")

answer = None
while answer not in ("y", "n", "a"):
	answer = raw_input("				\n\n		Do you want to proceed?			\n\n 			y - YES \n\n 			n - NO \n\n 			a - ADVANCED"		)
	
	
	
	if answer == "y":
		sleep(0.1)
		os.system("#sudo pkill server.py")
		os.system("#sudo systemctl stop rotorhazard")
		sleep(0.1)

		#GPIO.output(reset_1, #GPIO.LOW)
		#GPIO.output(reset_2, #GPIO.LOW)
		#GPIO.output(reset_3, #GPIO.LOW)
		#GPIO.output(reset_4, #GPIO.LOW)
		sleep(0.1)
		#GPIO.output(reset_1, #GPIO.HIGH)
		#GPIO.output(reset_2, #GPIO.HIGH)
		#GPIO.output(reset_3, #GPIO.HIGH)
		#GPIO.output(reset_4, #GPIO.HIGH)

		sleep(0.1)
		os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:node.hex:i")


		print("")
		print("				Node 1 - flashed")
		print("")
		print("")
		#GPIO.output(reset_1, #GPIO.LOW)
		#GPIO.output(reset_2, #GPIO.LOW)
		#GPIO.output(reset_3, #GPIO.LOW)
		#GPIO.output(reset_4, #GPIO.LOW)
		sleep(0.1)
		#GPIO.output(reset_1, #GPIO.HIGH)
		#GPIO.output(reset_2, #GPIO.HIGH)
		#GPIO.output(reset_3, #GPIO.HIGH)
		#GPIO.output(reset_4, #GPIO.HIGH)


		sleep(0.1)
		os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:node.hex:i")


		print("")
		print("				Node 2 - flashed")
		print("")
		print("")
		#GPIO.output(reset_1, #GPIO.LOW)
		#GPIO.output(reset_2, #GPIO.LOW)
		#GPIO.output(reset_3, #GPIO.LOW)
		#GPIO.output(reset_4, #GPIO.LOW)
		sleep(0.1)
		#GPIO.output(reset_1, #GPIO.HIGH)
		#GPIO.output(reset_2, #GPIO.HIGH)
		#GPIO.output(reset_3, #GPIO.HIGH)
		#GPIO.output(reset_4, #GPIO.HIGH)
		sleep(0.1)
		os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:node.hex:i")


		print("")
		print("				Node 3 - flashed")
		print("")
		print("")
		#GPIO.output(reset_1, #GPIO.LOW)
		#GPIO.output(reset_2, #GPIO.LOW)
		#GPIO.output(reset_3, #GPIO.LOW)
		#GPIO.output(reset_4, #GPIO.LOW)
		sleep(0.1)
		#GPIO.output(reset_1, #GPIO.HIGH)
		#GPIO.output(reset_2, #GPIO.HIGH)
		#GPIO.output(reset_3, #GPIO.HIGH)
		#GPIO.output(reset_4, #GPIO.HIGH)
		sleep(0.1)

		os.system("#sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
		os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:node.hex:i")
		os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")

		print("")
		print("				Node 4 - flashed")
		print("\n\n")
		sleep(0.1)
		print("			##########################################################################################")
		print("			###                                                                                    ###")
		print("			###             CONGRATULATIONS!            Flashing firmware to nodes - DONE          ###")
		print("			###                                                                                    ###")
		print("			###                                                                                    ###")
		print("			###    Please power off the timer, unplug voltage source for few seconds and reboot    ###")
		print("			###                                                                                    ###")
		print("			##########################################################################################")

		print("\n\n")
		sleep(1)
	elif answer == "n":
		print("")
		print("		OK - exiting")
		print("")	
	elif answer == "a":
		sleep(0.1)
		ans=True
		while ans:
			print("\n\n")
			print ("		1. Flash the bootloader")
			print ("		2. Fix GPIO pin state")
			print ("		3. Try to recover")
			print ("		4. Start the server")
			print ("		5. Show avrdude ")
			print ("		6. EXIT")
			print("\n")
			ans=raw_input("What would you like to do? ") 
			if ans=="1": 
					print("Attempting to flash a bootloader to Arduino") 
			elif ans=="2":
					os.system("echo 12 > /sys/class/#GPIO/unexport")
					os.system("echo 13 > /sys/class/#GPIO/unexport")
					os.system("echo 16 > /sys/class/#GPIO/unexport")
					os.system("echo 26 > /sys/class/#GPIO/unexport")
					os.system("echo 19 > /sys/class/#GPIO/unexport")
					os.system("echo 20 > /sys/class/#GPIO/unexport")
					os.system("echo 21 > /sys/class/#GPIO/unexport") 
					print("\n\nDONE\n\n")		
			elif ans=="3":
					print("\n Student Record Found")
					os.system("#sudo sed -i 's/reset .*/reset = 12;/g' /root/.avrduderc")
					os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:blank.hex:i")
					os.system("#sudo sed -i 's/reset .*/reset = 13;/g' /root/.avrduderc")
					os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:blank.hex:i")
					os.system("#sudo sed -i 's/reset .*/reset = 16;/g' /root/.avrduderc")
					os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:blank.hex:i")
					os.system("#sudo sed -i 's/reset .*/reset = 26;/g' /root/.avrduderc")
					os.system("#sudo avrdude -c linux#GPIO -p atmega328p -v -U flash:w:blank.hex:i")
			elif ans=="4":
					print("\n\nServer will start in 5 seconds\n\n")
					sleep(5)
					os.system("python ~/RotorHazard/src/server/server.py")	
			elif ans=="5":
					os.system("avrdude -c linuxgpio -p m328p -v")	
			elif ans=="6":
					print("\n\nSee you!\n\n")
					sys.exit()
			elif ans !="":
					print("\n\n Try again\n\n") 
		
	 
		# Flash the bootloader - usb support
							# Recover the Arduinos
							# Check the signatures
							# Fix pin busy
							# Program specific node
		 # pins fix
	else:
		print("")
		print("Please enter y / n / a")
		print("")