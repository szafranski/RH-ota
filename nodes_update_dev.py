from time import sleep
import os
import sys
import platform
import json
import update
from modules import clearTheScreen, bcolors, logoTop

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

if pins_assignment == 'PCB' or pins_assignment == 'pcb':
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

reset_list = [str(reset_1),str(reset_2),str(reset_3),str(reset_4),str(reset_5),str(reset_6),str(reset_7),str(reset_8)]

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

if (linux_testing == False): 
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)   # Use BCM pin numbering
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
		allPinsLow()
		sleep(0.1)
		allPinsHigh()

	def resetGPIO():
		allPinsReset()
		GPIO.output((reset_list[i]), GPIO.LOW)
		sleep(0.1)
		GPIO.output((reset_list[i]), GPIO.HIGH)

if (linux_testing == True): 

	for i in range(0, 8):
		print("GPIO.setup("+(reset_list[i])+", GPIO.OUT, initial=GPIO.HIGH)")
	sleep(0.5)
	
	def allPinsReset():
		print("\n\n\t\t\tallPinsReset")
		print("\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def allPinsLow():
		print("\n\n\t\t\tallPinsLow")
		for i in range(0, 8):
			print("GPIO.output("+(reset_list[i])+", GPIO.LOW")
		sleep(3)
	def allPinsHigh():
		print("\n\n\tallPinsHigh:")
		for i in range(0, 8):
			print("GPIO.output("+(reset_list[i])+", GPIO.HIGH")
		sleep(3)
	def resetGPIO():
		print("GPIO.output("+(reset_list[i])+", GPIO.LOW)")
		sleep(0.5)
		print("GPIO.output("+(reset_list[i])+", GPIO.HIGH)")

def logoUpdate():
	print("""
		#######################################################################
		###                                                                 ###
		###\t\t"""+bcolors.BOLD+"""Flashing firmware onto """+str(nodes_number)+""" nodes - DONE"""+bcolors.ENDC+"""\t\t    ###
		###                                                                 ###
		###                          """+bcolors.BOLD+"""Thank you!"""+bcolors.ENDC+"""                             ###
		###                                                                 ###
		#######################################################################
		\n\n""")

def flashAllNodes():
	global i
	for i in range(0, (nodes_number)):
		allPinsHigh()
		resetGPIO()
		print(reset_list[i])
		os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_"+str(i+1)+".hex:i ")
		print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_"+str(i+1)+".hex:i ")
		print("\n\n\t\t\t\t"+bcolors.BOLD+"Node "+str(i+1)+" - flashed"+bcolors.ENDC+"\n\n")
		sleep(1)

def flashAllGnd():
	global i
	for i in range(0, (nodes_number)):
		allPinsHigh()
		resetGPIO()
		print(reset_list[i])
		os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
		print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i ")
		print("\n\n\t\t\t\t"+bcolors.BOLD+"Node "+str(i+1)+" - flashed"+bcolors.ENDC+"\n\n")
		sleep(1)

def flashAllBlink():
	global i
	for i in range(0, (nodes_number)):
		allPinsHigh()
		resetGPIO()
		print(reset_list[i])
		os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
		print("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
		print("\n\n\t\t\t\t"+bcolors.BOLD+"Node "+str(i+1)+" - flashed"+bcolors.ENDC+"\n\n")
		sleep(1)

def flashEachNode():
	def nodeXMenu():
		global X
		print(bcolors.BOLD+"\n\t\t\t\t Node "+str(X)+" selected"+bcolors.ENDC)
		print(bcolors.BOLD+"\n\n\t\t Choose flashing type:\n"+bcolors.ENDC)
		print("\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
		print("\t\t 2 - Node ground-auto selection firmware")
		print("\t\t 3 - Flashes 'Blink' on the node")
		print("\t\t 4 - Abort")
		selection=str(raw_input(""))
		if selection=='1' :
			allPinsHigh()
			resetGPIO()
			if linux_testing == False:
				os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_"+str(X)+".hex:i ")
			else:
				print("\t\t\t/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_"+str(X)+".hex:i ")
			print(bcolors.BOLD+"\n\t Node "+str(X)+" flashed\n"+bcolors.ENDC)
			sleep(1)
			return
		if selection=='2' : 
			allPinsHigh()
			resetGPIO()
			os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/node_0.hex:i")
			print(bcolors.BOLD+"\n\t Node "+str(X)+" flashed\n"+bcolors.ENDC)
			sleep(1)
			return
		if selection=='3' : 
			allPinsHigh()
			resetGPIO()
			os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/firmware/"+firmware_version+"/blink.hex:i ")
			print(bcolors.BOLD+"\n\t Node "+str(X)+" flashed\n"+bcolors.ENDC)
			sleep(1)
			return
		if selection=='4':
			nodeMenu()
		if selection=='dev' : 
			allPinsHigh()
			resetGPIO()
			os.system("echo no_sudo &&  avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -U flash:w:/home/"+user+"/RH-ota/.dev/node_"+str(X)+".hex:i ")
			print(bcolors.BOLD+"\n\t Testing firmware on Node "+str(X)+" flashed\n"+bcolors.ENDC)
			sleep(1)
		else:
			nodeXMenu()
	def nodeMenu():
		global X
		clearTheScreen()
		logoTop()
		sleep(0.12)
		print("\n\n\n\t\t\t\t    "+bcolors.RED+bcolors.BOLD+"NODES MENU"+bcolors.ENDC)
		print("\n\t\t "+bcolors.BOLD+"1 - Flash node 1 \t\t 5 - Flash node 5"+bcolors.ENDC)
		print("\n\t\t "+bcolors.BOLD+"2 - Flash node 2 \t\t 6 - Flash node 6"+bcolors.ENDC)
		print("\n\t\t "+bcolors.BOLD+"3 - Flash node 3 \t\t 7 - Flash node 7"+bcolors.ENDC)
		print("\n\t\t "+bcolors.BOLD+"4 - Flash node 4 \t\t 8 - Flash node 8")
		print("\n\t\t\t\t"+bcolors.YELLOW+bcolors.BOLD+"e - Exit to main menu"+bcolors.ENDC)
		selection=str(raw_input("\n\n\t\t"+bcolors.BOLD+"Which node do you want to program:"+bcolors.ENDC+" "))
		print("\n\n")
		if(selection.isdigit()) and int(selection) <=8:
			X=selection
			sleep(0.5)
			nodeXMenu()
		if selection=='e':
			nodesUpdate()
		else:
			nodeMenu()
	nodeMenu()

def gpioState(): 
	clearTheScreen()
	logoTop()
	print("\n\n\n")
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
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 1:
		# return
	# nodeTwoReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 2:
		# return
	# nodeThreeReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 3:
		# return
	# nodeFourReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 4:
		# return
	# nodeFiveReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 5:
		# return
	# nodeSixReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 6:
		# return
	# nodeSevenReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 7:
		# return
	# nodeEightReset()
	# os.system("echo no_sudo &&  avrdude -c arduino -p m328p -v")
	# sleep(2)
	# if nodes_number == 8:
		# return

def nodesUpdate():
	clearTheScreen()
	logoTop()
	sleep(0.12)
	print("\n\n\t\t\t "+bcolors.BOLD+bcolors.UNDERLINE+"CHOOSE FLASHING TYPE:\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.GREEN+bcolors.BOLD+"1 - Every Node gets own dedicated firmware - recommended\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.BOLD+"2 - Nodes will use ground-auto selection firmware\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.BOLD+"3 - Flash 'Blink' on every node\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.BOLD+"4 - Flash each node individually\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.BOLD+"5 - I2C programming - early beta\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.BOLD+"6 - Fix GPIO pins state - obsolete\n"+ bcolors.ENDC)
	print("\t\t "+bcolors.YELLOW+bcolors.BOLD+"e - Exit to main menu\n"+ bcolors.ENDC)
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
		os.system("python ./.dev/i2c_nodes_py")
	if selection=='6':
		gpioState()
	if selection=='e':
		sys.exit()
	else:
		nodesUpdate()
nodesUpdate()
