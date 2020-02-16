####To do:####

# pins low/high as a function
# define number of pins
# 'flashed' - only after success 


######## enter pins connected to reset pins on Arduinos ########
reset_1 = 12  # node 1
reset_2 = 13  # node 2
reset_3 = 16  # node 3
reset_4 = 26  # node 4


import RPi.GPIO as GPIO
from time import sleep
import os
import sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(reset_2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(reset_3, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(reset_4, GPIO.OUT, initial=GPIO.HIGH)


def mainMenu():
	os.system("clear")
	sleep(0.2)
	print("\n\n\n")	
	print("		############################################################################################")
	print("		###                                                                                      ###")
	print("		###                                 RotorHazard                                          ###")
	print("		###                                                                                      ###")
	print("		###    You are about to update nodes firmware. Please do not interrupt this operation!   ###")
	print("		###                                                                                      ###")
	print("		###                                                                                      ###")
	print("		############################################################################################")



	print("\n\n\n\t What do you want to do now:\n\n")
	print("\t\t 1 - Nodes flash and update")
	print("\t\t 2 - Advanced menu")
	print("\t\t 3 - Exit")
	print("\t\t 4 - This is my first time - READ!\n\n")
	selection=str(raw_input(""))
	if selection=='1':
		update()
	if selection=='2':
		advanced()
	if selection=='3':
		exit()
	if selection=='4':
		first()	
	else: 
		mainMenu()	

def update():
	print("\n\n\t Choose flashing type\n")
	print("\t '1' - Nodes get own dedicated firmware")
	print("\t '2' - Nodes ground-autoselectionfirmware")
	print("\t '3' - Flashes 'blank' hex on every node")
	print("\t '4' - Go back")
	sleep(0.1)
	selection=str(raw_input(""))
	if selection=='1':
		programming_type = 1
	if selection=='2':
		programming_type = 2	
	if selection=='3':
		programming_type = 3
	if selection=='4':
		mainMenu()
		
	os.system("sudo pkill server.py")
	os.system("sudo systemctl stop rotorhazard")
	sleep(0.1)

	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)

	sleep(0.1)
	os.system("sudo sed -i 's/reset .#/reset = 12;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_1.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 1 - flashed")
	print("\n\n")

	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)


	sleep(0.1)
	os.system("sudo sed -i 's/reset .#/reset = 13;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_2.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 2 - flashed")
	print("\n\n")

	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)
	sleep(0.1)
	os.system("sudo sed -i 's/reset .#/reset = 16;/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_3.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 3 - flashed")
	print("\n\n")

	GPIO.output(reset_1, GPIO.LOW)
	GPIO.output(reset_2, GPIO.LOW)
	GPIO.output(reset_3, GPIO.LOW)
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.1)
	GPIO.output(reset_1, GPIO.HIGH)
	GPIO.output(reset_2, GPIO.HIGH)
	GPIO.output(reset_3, GPIO.HIGH)
	GPIO.output(reset_4, GPIO.HIGH)
	sleep(0.1)

	if programming_type ==1 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
	os.system("sudo sed -i 's/reset .#/reset = 12;/g' /root/.avrduderc")
	sleep(0.3)

	print("")
	print("				Node 4 - flashed")
	print("\n\n")
	sleep(0.1)
	print("		##########################################################################################")
	print("		###                                                                                    ###")
	print("		###             CONGRATULATIONS!             Flashing firmware to nodes -    DONE      ###")
	print("		###                                                                                    ###")
	print("		###                                                                                    ###")
	print("		###    Please power off the timer, unplug voltage source for few seconds and reboot    ###")
	print("		###                                                                                    ###")
	print("		##########################################################################################")
	print("\n\n")
	sleep(5)
def exit():
	sleep(0.2)
	print("\n\nSee you!\n\n")
	sys.exit()
def advanced():
	sleep(0.1)
	def advancedMenu():
		print("\n\n\n")
		print("\n			ADVANCED MENU:\n")
		print("		'1' - Flash the bootloader")
		print("		'2' - Fix GPIO pins state")
		print("		'3' - Try to recover")
		print("		'4' - Start the server")
		print("		'5' - Install / check avrdude")
		print("		'6' - Program specific node")
		print("		'7' - Enter main menu")
		print("\n")
			
		selection=str(raw_input(""))
		if selection=='1':
			bootloader()
		if selection=='2':
			gpio_fix()
		if selection=='3':
			recover()		
		if selection=='4':
			server_start()
		if selection=='5':
			avr_info()
		if selection=='6':
			program_node()
		if selection=='7':
			sleep(0.2)	
			mainMenu()
		else:
			sleep(0.1) 
			advancedMenu()
	def bootloader(): 
		def bootMenu():
			print("\n\t\t NODE MENU")
			print("\n\t 1 - Flash bootloader on node 1")
			print("\n\t 2 - Flash bootloader on node 2")
			print("\n\t 3 - Flash bootloader on node 3")
			print("\n\t 4 - Flash bootloader on node 4")
			print("\n\t 5 - Go back")
			selection=str(raw_input("\n\nWhich node do you want to flash bootloader on: "))
			if selection=='1':
				print("\n\t Node 1 selected")
				os.system("sudo sed -i 's/reset .#/reset = 12;/g' /root/.avrduderc")
				os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Bootloader flashed")
			if selection=='2':
				os.system("sudo sed -i 's/reset .#/reset = 13;/g' /root/.avrduderc")
				print("\n\t Node 2 selected")	
				os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Bootloader flashed")
			if selection=='3':
				print("\n\t Node 3 selected")	
				os.system("sudo sed -i 's/reset .#/reset = 16;/g' /root/.avrduderc")
				os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Bootloader flashed")
			if selection=='4':
				print("\n\t Node 4 selected")		
				os.system("sudo sed -i 's/reset .#/reset = 26;/g' /root/.avrduderc")
				os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")		
				print("\n\t Bootloader flashed")
			if selection=='5':
				advancedMenu()
		bootMenu()
	def gpio_fix(): 
		os.system("echo 12 > /sys/class/GPIO/unexport")
		os.system("echo 13 > /sys/class/GPIO/unexport")
		os.system("echo 16 > /sys/class/GPIO/unexport")
		os.system("echo 26 > /sys/class/GPIO/unexport")
		os.system("echo 19 > /sys/class/GPIO/unexport")
		os.system("echo 20 > /sys/class/GPIO/unexport")
		os.system("echo 21 > /sys/class/GPIO/unexport") 
		print("\n\n		DONE\n\n")		
	def recover():
		print("\n 		Attempting recovery\n\n")
		os.system("sudo sed -i 's/reset .#/reset = 12;/g' /root/.avrduderc")
		os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("sudo sed -i 's/reset .#/reset = 13;/g' /root/.avrduderc")
		os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("sudo sed -i 's/reset .#/reset = 16;/g' /root/.avrduderc")
		os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:blank.hex:i")
		os.system("sudo sed -i 's/reset .#/reset = 26;/g' /root/.avrduderc")
		os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:blank.hex:i")
	def server_start():
		print("\n\n   Server will start in 5 seconds\n\n")
		print("\n\n		Please wait...\n\n")
		print("\n")
		sleep(4)
		os.system("sudo pkill server.py")
		os.system("sudo systemctl stop rotorhazard")
		os.system("python ~/RotorHazard/src/server/server.py")	
	def avr_info():
		print("\n			What do you want to do:\n")
		print ("		'1' - Check the state of avrdude installation + config file")
		print ("		'2' - Check if nodes (at least one) are connected properly ")
		print ("		'3' - Install avrdude")
		print ("		'4' - Go back")
		selection=str(raw_input(""))
		if selection=='1' : 
			os.system("sudo avrdude -v")
		if selection=='2' : 
			os.system("sudo avrdude -c linuxGPIO -p m328p -v")
		if selection=='3' : 
			os.system("sudo apt-get update")	
			os.system("sudo apt-get install wget bison flex -y")			
			os.chdir("/home/pi")			
			os.system("wget http://download.savannah.gnu.org/releases/avrdude/avrdude-6.2.tar.gz")			
			os.system("tar xfv avrdude-6.2.tar.gz")			
			os.chdir("/home/pi/avrdude-6.2/")	
			os.system("./configure --enable-linuxgpio")	
			os.system("make")			
			os.system("sudo cp programmer.txt /home/pi/.avrduderc")
			# os.system("rm /home/pi/.avrduderc")			
			# os.system("echo 'programmer'| sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' id    = "linuxgpio";| sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' desc  = "Use the Linux sysfs interface to bitbang GPIO lines";| sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' type  = "linuxgpio";| sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' reset = 12; ' | sudo tee -a /home/pi/.avrduderc")
			# os.system("echo ' sck   = 21;' | sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' mosi  = 20;' | sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' miso  = 19;' | sudo  tee -a /home/pi/.avrduderc")
			# os.system("echo ' ;' | sudo  tee -a /home/pi/.avrduderc")
			os.system("sudo avrdude -v")	
		if selection=='4' : 
			advancedMenu()
		avr_info()
	def program_node():
		def nodeMenu():
			print("\n\t\t NODE MENU")
			print("\n\t 1 - Flash node 1")
			print("\n\t 2 - Flash node 2")
			print("\n\t 3 - Flash node 3")
			print("\n\t 4 - Flash node 4")
			print("\n\t 5 - Go back")
			selection=str(raw_input("\n\nWhich node do you want to program: "))
			if selection=='1':
				os.system("sudo sed -i 's/reset .#/reset = 12;/g' /root/.avrduderc")
				print("\n\t Node 1 selected")	
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - Node gets own dedicated firmware")
				print("\t '2' - Node ground-autoselectionfirmware")
				print("\t '3' - Flashes 'blank' hex on the node")
				print("\t '4' - Flashes bootloader on the node")
				print("\t '5' - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_1.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection=='4' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
				if selection=='5':
					nodeMenu()
			if selection=='2':
				os.system("sudo sed -i 's/reset .#/reset = 13;/g' /root/.avrduderc")
				print("\n\t Node 2 selected")	
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - Node gets own dedicated firmware")
				print("\t '2' - Node ground-autoselectionfirmware")
				print("\t '3' - Flashes 'blank' hex on the node")
				print("\t '4' - Flashes bootloader on the node")
				print("\t '5' - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_2.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection=='4' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
				if selection=='5':
					nodeMenu()
			if selection=='3':
				os.system("sudo sed -i 's/reset .#/reset = 16;/g' /root/.avrduderc")
				print("\n\t Node 3 selected")	
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - Node gets own dedicated firmware")
				print("\t '2' - Node ground-autoselectionfirmware")
				print("\t '3' - Flashes 'blank' hex on the node")
				print("\t '4' - Flashes bootloader on the node")
				print("\t '5' - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_3.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection=='4' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
				if selection=='5':
					nodeMenu()
			if selection=='4':
				os.system("sudo sed -i 's/reset .#/reset = 26;/g' /root/.avrduderc")
				print("\n\t Node 4 selected")	
				print("\n\n\t Choose flashing type\n")
				print("\t '1' - Node gets own dedicated firmware")
				print("\t '2' - Node ground-autoselectionfirmware")
				print("\t '3' - Flashes 'blank' hex on the node")
				print("\t '4' - Flashes bootloader on the node")
				print("\t '5' - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.hex:i")
				if selection=='4' : 
					os.system("sudo avrdude -c linuxGPIO -p m328p -v -U flash:w:firmware/blank.b.hex:i")	
				print("\n\t Node flashed")
				if selection=='5':
					nodeMenu()
			if selection=='5':
				sleep(0.2)	
				advancedMenu()
				nodeMenu()	
		nodeMenu()			
	advancedMenu()
def first():
	os.system("clear")
	sleep(0.1)
	print("\n\n\n\t\t Hello! You are using tool designed to easy uploadig the firmware on the RotorHazard racetimer nodes.")
	print("\n\t\t For now consider this tool as a beta verision. Tests are being done constantly.")
	print("\n\n ")
	print("\n\t\t Files that you are about to flash are 'hex' files from an official RotorHazard Arduino nodes ino files.")
	print("\n\t\t After using this tool nodes would be flashed WITHOUT the bootloader which means,")
	print("\n\t\t that you won't be capable of connecting your Arduinos to the usb port and using it with PC anymore,")
	print("\n\t\t unless you flash bootloader back using 'Advanced menu' of this software.")
	print("\n\n ")
	print("\n\t\t It is recommended to flash nodes with specfic file for every node, even if you are using autoselectionmod.")
	print("\n\t\t This way you can allways check if nodes were flashed correctly during manual boot of the server file ")
	print("\n\t\t  - what smartass would do after flashing new firmware anyway. ")
	print("\n ")
	print("\n\t\t If you are using this tool for the first time enter 'Advanced menu' and select 'Install avrdude'.")
	print("\n\t\t For more hardware instructions open 'manuals' file or visit Facebook page.")
	print("\n ")
	print("\n\n\t\t  Enjoy!\t\t\t\t\t\t\t\t Szafran\n\n ")
	selection=str(raw_input("\t\t\t\t\t\tGo back by pressing 'b'\n"))
	if selection=='b':
		mainMenu()
	else :
		first()
mainMenu()
