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

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

if os.path.exists("./updater-config.json") == True:
	if check_if_string_in_file('updater-config.json', 'assignment'):
		pins_assignment = data['pins_assignment']
	else:
		pins_assignment = 'default'
else:
	pins_assignment = 'default'

preffered_RH_version = data['RH_version']

if preffered_RH_version == 'master':
	firmware_version = 'master'
if preffered_RH_version == 'beta':
	firmware_version = 'beta'
if preffered_RH_version == 'stable':
	firmware_version = 'stable'
if preffered_RH_version == 'custom':
	firmware_version = 'stable'

nodes_number = data['nodes_number']

if pins_assignment == 'PCB':
	reset_1 = 12    ## node 1   # default 12
	reset_2 = 16    ## node 2   # default 16
	reset_3 = 4     ## node 3   # default 4
	reset_4 = 21    ## node 4   # default 21
	reset_5 = 6     ## node 5   # default 6
	reset_6 = 13    ## node 6   # default 13
	reset_7 = 19    ## node 7   # default 19
	reset_8 = 26    ## node 8   # default 26
if pins_assignment == 'default':
	reset_1 = 12    ## node 1   # default 12
	reset_2 = 16    ## node 2   # default 16
	reset_3 = 20    ## node 3   # default 20
	reset_4 = 21    ## node 4   # default 21
	reset_5 = 6     ## node 5   # default 6
	reset_6 = 13    ## node 6   # default 13
	reset_7 = 19    ## node 7   # default 19
	reset_8 = 26    ## node 8   # default 26
if pins_assignment == 'custom':
	reset_1 = 0    ## node 1   # custom pin assignment
	reset_2 = 0    ## node 2   # custom pin assignment
	reset_3 = 0    ## node 3   # custom pin assignment
	reset_4 = 0    ## node 4   # custom pin assignment
	reset_5 = 0    ## node 5   # custom pin assignment
	reset_6 = 0    ## node 6   # custom pin assignment
	reset_7 = 0    ## node 7   # custom pin assignment
	reset_8 = 0    ## node 8   # custom pin assignment

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

class bcolors:
	HEADER = '\033[95m'
	ORANGE = '\033[33m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

if (linux_testing == False): 
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM) # Use BCM pin numbering
	GPIO.setup(reset_1, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_2, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_3, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_4, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_5, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_6, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_7, GPIO.OUT, initial=GPIO.HIGH)
	GPIO.setup(reset_8, GPIO.OUT, initial=GPIO.HIGH)

	def allPinsLow():
		GPIO.output(reset_1, GPIO.LOW)
		GPIO.output(reset_2, GPIO.LOW)
		GPIO.output(reset_3, GPIO.LOW)
		GPIO.output(reset_4, GPIO.LOW)
		GPIO.output(reset_5, GPIO.LOW)
		GPIO.output(reset_6, GPIO.LOW)
		GPIO.output(reset_7, GPIO.LOW)
		GPIO.output(reset_8, GPIO.LOW)
		sleep(0.05)

	def allPinsHigh():
		GPIO.output(reset_1, GPIO.HIGH)
		GPIO.output(reset_2, GPIO.HIGH)
		GPIO.output(reset_3, GPIO.HIGH)
		GPIO.output(reset_4, GPIO.HIGH)
		GPIO.output(reset_5, GPIO.HIGH)
		GPIO.output(reset_6, GPIO.HIGH)
		GPIO.output(reset_7, GPIO.HIGH)
		GPIO.output(reset_8, GPIO.HIGH)
		sleep(0.05)

	def allPinsReset():
		GPIO.output(reset_1, GPIO.LOW)
		GPIO.output(reset_2, GPIO.LOW)
		GPIO.output(reset_3, GPIO.LOW)
		GPIO.output(reset_4, GPIO.LOW)
		GPIO.output(reset_5, GPIO.LOW)
		GPIO.output(reset_6, GPIO.LOW)
		GPIO.output(reset_7, GPIO.LOW)
		GPIO.output(reset_8, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_1, GPIO.HIGH)
		GPIO.output(reset_2, GPIO.HIGH)
		GPIO.output(reset_3, GPIO.HIGH)
		GPIO.output(reset_4, GPIO.HIGH)
		GPIO.output(reset_5, GPIO.HIGH)
		GPIO.output(reset_6, GPIO.HIGH)
		GPIO.output(reset_7, GPIO.HIGH)
		GPIO.output(reset_8, GPIO.HIGH)

	def nodeOneReset():
		allPinsHigh()
		GPIO.output(reset_1, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_1, GPIO.HIGH)
	def nodeTwoReset():
		allPinsHigh()
		GPIO.output(reset_2, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_2, GPIO.HIGH)
	def nodeThreeReset():
		allPinsHigh()
		GPIO.output(reset_3, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_3, GPIO.HIGH)
	def nodeFourReset():
		allPinsHigh()
		GPIO.output(reset_4, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_4, GPIO.HIGH)
	def nodeFiveReset():
		allPinsHigh()
		GPIO.output(reset_5, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_5, GPIO.HIGH)
	def nodeSixReset():
		allPinsHigh()
		GPIO.output(reset_6, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_6, GPIO.HIGH)
	def nodeSevenReset():
		allPinsHigh()
		GPIO.output(reset_7, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_7, GPIO.HIGH)
	def nodeEightReset():
		allPinsHigh()
		GPIO.output(reset_8, GPIO.LOW)
		sleep(0.1)
		GPIO.output(reset_8, GPIO.HIGH)

if (linux_testing == True): 
	def allPinsReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def allPinsLow():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def allPinsHigh():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeOneReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeTwoReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeThreeReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeFourReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeFiveReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeSixReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeSevenReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeEightReset():
		print("\n\n\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/X.hex")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)

def logoTop():
	print("""\n	
		#######################################################################
		###                                                                 ###
		###\t\t\t"""+bcolors.ORANGE+"""     RotorHazard        """+bcolors.ENDC+"""\t\t    ###
		###                                                                 ###
		###                     OTA Updater and Manager                     ###
		###                                                                 ###
		#######################################################################""")
	if (linux_testing == True):
		print("\t\t\t  Linux PC version\t"+"Pins assignment mode: "+str(pins_assignment))
	if os.path.exists("./updater-config.json") == False:
		print("\t\t\t    Looks that you haven't set up config file yet!")

def logoUpdate():
	print("""
		#######################################################################
		###                                                                 ###
		###\t\tFlashing firmware onto """+str(nodes_number)+""" nodes - DONE\t\t    ###
		###                                                                 ###
		###                          Thank you!                             ###
		###                                                                 ###
		#######################################################################
		\n\n""")

def flashAllNodes():
	nodeOneReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_1.hex:i ")
	print("\n				Node 1 - flashed\n\n")
	sleep(1)
	if nodes_number ==1:
		return
	nodeTwoReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_2.hex:i ")
	print("\n				Node 2 - flashed\n\n")
	sleep(1)
	if nodes_number ==2:
		return
	nodeThreeReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_3.hex:i ")
	print("\n				Node 3 - flashed\n\n")
	sleep(1)
	if nodes_number ==3:
		return
	nodeFourReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_4.hex:i ")
	print("\n				Node 4 - flashed\n\n")
	sleep(1)
	if nodes_number ==4:
		return
	nodeFiveReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_5.hex:i ")
	print("\n				Node 5 - flashed\n\n")
	sleep(1)
	if nodes_number ==5:
		return
	nodeSixReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_6.hex:i ")
	print("\n				Node 6 - flashed\n\n")
	sleep(1)
	if nodes_number ==6:
		return
	nodeSevenReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_7.hex:i ")
	print("\n				Node 7 - flashed\n\n")
	sleep(1)
	if nodes_number ==7:
		return
	nodeEightReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_8.hex:i ")
	print("\n				Node 8 - flashed\n\n")
	if nodes_number ==8:
		return

def flashAllGnd():
	nodeOneReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 1 - flashed\n\n")
	sleep(1)
	if nodes_number ==1:
		return
	nodeTwoReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 2 - flashed\n\n")
	sleep(1)
	if nodes_number ==2:
		return
	nodeThreeReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 3 - flashed\n\n")
	sleep(1)
	if nodes_number ==3:
		return
	nodeFourReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 4 - flashed\n\n")
	sleep(1)
	if nodes_number ==4:
		return
	nodeFiveReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 5 - flashed\n\n")
	sleep(1)
	if nodes_number ==5:
		return
	nodeSixReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 6 - flashed\n\n")
	sleep(1)
	if nodes_number ==6:
		return
	nodeSevenReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 7 - flashed\n\n")
	sleep(1)
	if nodes_number ==7:
		return
	nodeEightReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
	print("\n				Node 8 - flashed\n\n")
	sleep(1)
	if nodes_number ==8:
		return

def flashAllBlink():
	nodeOneReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 1 - flashed\n\n")
	sleep(1)
	if nodes_number ==1:
		return
	nodeTwoReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 2 - flashed\n\n")
	sleep(1)
	if nodes_number ==2:
		return
	nodeThreeReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 3 - flashed\n\n")
	sleep(1)
	if nodes_number ==3:
		return
	nodeFourReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 4 - flashed\n\n")
	sleep(1)
	if nodes_number ==4:
		return
	nodeFiveReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 5 - flashed\n\n")
	sleep(1)
	if nodes_number ==5:
		return
	nodeSixReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 6 - flashed\n\n")
	sleep(1)
	if nodes_number ==6:
		return
	nodeSevenReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 7 - flashed\n\n")
	sleep(1)
	if nodes_number ==7:
		return
	nodeEightReset()
	os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
	print("\n				Node 8 - flashed\n\n")
	sleep(1)
	if nodes_number ==8:
		return

def flashEachNode():
	def nodeMenu():
		sleep(0.12)
		os.system("clear")
		sleep(0.12)
		logoTop()
		sleep(0.12)
		print("\n\n\n\t\t\t\t\t    "+bcolors.RED+"NODES MENU"+bcolors.ENDC)
		print("\n\t\t\t 1 - Flash node 1 \t\t 5 - Flash node 5")
		print("\n\t\t\t 2 - Flash node 2 \t\t 6 - Flash node 6")
		print("\n\t\t\t 3 - Flash node 3 \t\t 7 - Flash node 7")
		print("\n\t\t\t 4 - Flash node 4 \t\t 8 - Flash node 8")
		print("\n\t\t\t\t\t"+bcolors.YELLOW+"9 - Back to main menu"+bcolors.ENDC)
		selection=str(raw_input("\n\n\t\t\tWhich node do you want to program: "))
		print("\n\n")
		if selection=='1':
			def nodeOneMenu():
				print("\n\t\t\t\t Node 1 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeOneReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_1.hex:i ")
					print("\n\t Node 1 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeOneReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 1 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeOneReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 1 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				if selection=='55' : 
					nodeOneReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/comm.hex:i ")
					print("\n\t Testing firmware on Node 1 flashed\n")
					sleep(1.5)
				else:
					nodeOneMenu()
				nodeMenu()
			nodeOneMenu()
		if selection=='2':
			def nodeTwoMenu():
				print("\n\t\t\t\t Node 2 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeTwoReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_2.hex:i ")
					print("\n\t Node 2 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeTwoReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeTwoReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 2 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeTwoMenu()
				nodeMenu()
			nodeTwoMenu()
		if selection=='3':
			def nodeThreeMenu():
				print("\n\t\t\t\t Node 3 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeThreeReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_3.hex:i ")
					print("\n\t Node 3 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeThreeReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 3 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeThreeReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 3 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeThreeMenu()
				nodeMenu()
			nodeThreeMenu()
		if selection=='4':
			def nodeFourMenu():
				print("\n\t\t\t\t Node 4 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeFourReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_4.hex:i ")
					print("\n\t Node 4 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeFourReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 4 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeFourReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 4 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeFourMenu()
				nodeMenu()
			nodeFourMenu()
		if selection=='5':
			def nodeFiveMenu():
				print("\n\t\t\t\t Node 5 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeFiveReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_5.hex:i ")
					print("\n\t Node 5 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeFiveReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 5 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeFiveReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 5 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeFiveMenu()
				nodeMenu()
			nodeFiveMenu()
		if selection=='6':
			def nodeSixMenu():
				print("\n\t\t\t\t Node 6 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeSixReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_6.hex:i ")
					print("\n\t Node 6 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeSixReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 6 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeSixReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 6 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeSixMenu()
				nodeMenu()
			nodeSixMenu()
		if selection=='7':
			def nodeSevenMenu():
				print("\n\t\t\t\t Node 7 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_7.hex:i ")
					print("\n\t Node 7 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 7 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 7 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeSevenMenu()
				nodeMenu()
			nodeSevenMenu()
		if selection=='8':
			def nodeEightMenu():
				print("\n\t\t\t\t Node 8 selected")
				print("\n\n\t\t\t Choose flashing type:\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'Blink' on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_8.hex:i ")
					print("\n\t Node 8 flashed\n")
					sleep(1.5)
					return
				if selection=='2' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
					print("\n\t Node 8 flashed\n")
					sleep(1.5)
					return
				if selection=='3' : 
					nodeSevenReset()
					os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
					print("\n\t Node 8 flashed\n")
					sleep(1.5)
					return
				if selection=='4':
					nodeMenu()
				else:
					nodeEightMenu()
				nodeMenu()
			nodeEightMenu()
		if selection=='9':
			sys.exit()
		else:
			nodeMenu()
	nodeMenu()

def gpioState(): 
	os.system("clear")
	logoTop()
	print("/n/n/n")
	os.system("echo "+str(reset_1)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_2)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_3)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_4)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_5)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_6)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_7)+" > /sys/class/GPIO/unexport")
	os.system("echo "+str(reset_8)+" > /sys/class/GPIO/unexport")
	os.system("echo 19 > /sys/class/GPIO/unexport")
	os.system("echo 20 > /sys/class/GPIO/unexport")
	os.system("echo 21 > /sys/class/GPIO/unexport") 
	print("\n\n		DONE\n\n")
	sleep(0.3)

# def connectionTest(): 
	# nodeOneReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 1:
		# return
	# nodeTwoReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 2:
		# return
	# nodeThreeReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 3:
		# return
	# nodeFourReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 4:
		# return
	# nodeFiveReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 5:
		# return
	# nodeSixReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 6:
		# return
	# nodeSevenReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 7:
		# return
	# nodeEightReset()
	# os.system("sudo avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 8:
		# return

def nodesUpdate():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\t\t\t\t Choose flashing type:\n")
	print("\t\t\t "+bcolors.GREEN+"1 - Every Node gets own dedicated firmware - recommended"+ bcolors.ENDC+"\n")
	print("\t\t\t 2 - Nodes will use ground-auto selection firmware\n")
	print("\t\t\t 3 - Flash 'Blink' on every node\n")
	print("\t\t\t 4 - Flash each node individually\n")
	print("\t\t\t 5 - I2C programming - early beta\n")
	print("\t\t\t 6 - Fix GPIO pins state - obsolete\n")
	print("\t\t\t "+bcolors.YELLOW+"7 - Go back"+bcolors.ENDC+"\n")
	sleep(0.3)
	selection=str(raw_input(""))
	if selection=='1':
		flashAllNodes()
		logoUpdate()
		sleep(3)
	if selection=='2':
		flashAllGnd()
		logoUpdate()
		sleep(3)
	if selection=='3':
		flashAllBlink()
		logoUpdate()
		sleep(3)
	if selection=='4':
		flashEachNode()
	if selection=='5':
		os.system("python ./i2c_nodes_update.py")
	if selection=='6':
		gpioState()
	if selection=='7':
		sys.exit()
	else:
		nodesUpdate()
nodesUpdate()