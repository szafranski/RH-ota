####To do:####

# show 'flashed' - only after success?
# define number of nodes
# Access Point
# self-updater

##### Change those only if you want to test the software on PC #####
linux_testing = False  		### change to True for testing on Linux PC or WSL
							### change your Linux PC username in line 99 as well

########    Enter pins connected to reset pins on Arduino-nodes:    ########

reset_1 = 12  ## node 1  # 12
reset_2 = 16  ## node 2  # 16
reset_3 = 20  ## node 3  # 20
reset_4 = 21  ## node 4  # 21
reset_5 = 6   ## node 5  # 6
reset_6 = 13  ## node 6  # 13
reset_7 = 19  ## node 7  # 19
reset_8 = 26  ## node 8  # 26

if (linux_testing == False):
	user = 'pi'           ### you can change it if your Raspberry's user is named differently

if (linux_testing == True):
	linux_user = 'pfabi'   ### change this if you are using this software on Linux PC for testing
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

from time import sleep
import os
import sys


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
	user= linux_user   
	def allPinsReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def allPinsLow():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def allPinsHigh():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeOneReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeTwoReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeThreeReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeFourReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeFiveReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeSixReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeSevenReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)
	def nodeEightReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.3)

def image():
	print("""
\t\t                               **/(((/**                              
\t\t                            */###########(*                           
\t\t                          */#####@@@@@#####(*                         
\t\t                         *(((((@@@###@@@#####*,                       
\t\t                       */((((@@@#######@@@####/*                      
\t\t                      *(((((@@@(((((#(##@@@#####*                     
\t\t                    **((((&@@&((((*...####@@@####**                   
\t\t                   *(((((@@@((((((....((((#@@@#####*                  
\t\t                 **((((#@@@((((((*.....((((#%@@&####/*                
\t\t                */((((@@@((((((((......(((((((@@@####(*               
\t\t              .*(((((@@@(((((((((......((((((((@@@%####**             
\t\t             */((((@@@(((((((((((......((((((((((@@@####(*            
\t\t            *(((((@@@((((((((((((.....*(((((((((((@@@#####*,          
\t\t          **((((@@@((((((((((((((.....((((((((((((((@@@(#(#/*         
\t\t          *((((@@@(((((((((((((((.....(((((((((((((((@@@((###*        
\t\t       */((((&@@&(((((((((((((,...(((....(((((((((((((#@@@((((/*      
\t\t      */((((@@@(((((((((......................((((((((((@@@((((#*     
\t\t    .*//(((@@@((((((............(((((((*.........,(((((((%@@&((((/*   
\t\t   */////@@@(((((........../((((((((((((((*..........((((((@@@(((((*  
\t\t  */////@@@/(((......./(((((((((((((((((((((((/......../((((@@@#((((*.
\t\t *////%@@/////(((((((((((((((((((((((((((((((((((((((..(((((((@@@((((*
\t\t *////@@@/////////((((((((((((((((((((((((((((((((((((((((((((@@@((((*
\t\t **/////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((**
\t\t  ***/////////////////(((((((((((((((((((((((((((((((((((((((((((((** 
\t\t     ****////////////////((((((((((((((((((((((((((((((((((((/****   
""")

def logo():
	print("""\n\n	
		#######################################################################
		###                                                                 ###
		###                        """+bcolors.ORANGE+"""RotorHazard"""+bcolors.ENDC+"""                              ###
		###                                                                 ###
		###                   OTA Updater and Manager                       ###
		###                                                                 ###
		#######################################################################""")

def logo2():
	print("""
		#######################################################################
		###                                                                 ###
		###                Flashing firmware to nodes - DONE                ###
		###                                                                 ###
		###                          Thank you!                             ###
		###                                                                 ###
		#######################################################################
		\n\n""")

def first ():
	image ()
	os.system("clear")
	print("\n\n\n\n\n")
	image()
	sleep(1.3)
first()

def flashEachNode():
	def nodeMenu():
		os.system("clear")
		logo()
		print("\n\n\n\t\t\t\t\t    "+bcolors.RED+"NODE MENU"+bcolors.ENDC)
		print("\n\t\t\t 1 - Flash node 1 \t\t 5 - Flash node 5")
		print("\n\t\t\t 2 - Flash node 2 \t\t 6 - Flash node 6")
		print("\n\t\t\t 3 - Flash node 3 \t\t 7 - Flash node 7")
		print("\n\t\t\t 4 - Flash node 4 \t\t 8 - Flash node 8")
		print("\n\t\t\t              "+bcolors.YELLOW+"9 - Back to main menu"+bcolors.ENDC)
		selection=str(raw_input("\n\n\t\t\tWhich node do you want to program: "))
		print("\n\n")
		if selection=='1':
			print("\n\t\t\t\t Node 1 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_1.hex:i ")
			if selection=='2' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='2':
			print("\n\t\t\t\t Node 2 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_2.hex:i ")
			if selection=='2' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='3':
			print("\n\t\t\t\t Node 3 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_3.hex:i ")
			if selection=='2' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='4':
			print("\n\t\t\t\t Node 4 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_4.hex:i ")
			if selection=='2' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='5':
			print("\n\t\t\t\t Node 5 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_5.hex:i ")
			if selection=='2' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='6':
			print("\n\t\t\t\t Node 6 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_6.hex:i ")
			if selection=='2' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='7':
			print("\n\t\t\t\t Node 7 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_7.hex:i ")
			if selection=='2' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='8':
			print("\n\t\t\t\t Node 8 selected")
			print("\n\n\t\t\t Choose flashing type:\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_8.hex:i ")
			if selection=='2' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='9':
			mainMenu()
	nodeMenu()

def mainMenu():
	os.system("clear")
	logo()
	if linux_testing == False:
		os.system("sudo systemctl stop rotorhazard")
	print("\n\n\n\t\t\t\t\t "+bcolors.RED+"   MAIN MENU\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"1 - Server software installation and update\n	"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("\t\t\t   3 - Start the server now\n")
	print("\t\t\t   4 - Additional features\n")
	print("\t\t\t   5 - This is my first time - READ!\n")
	print("\t\t\t   "+bcolors.YELLOW+"6 - Exit"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1':
		sleep(0.3)
		os.system('python ./rpi_soft.py')
	if selection=='2':
		def nodesUpdate():
			os.system("clear")
			logo()
			print("\n\n\t\t\t\t Choose flashing type:\n")
			print("\t\t\t "+bcolors.GREEN+"1 - Every Node gets own dedicated firmware - recommended"+ bcolors.ENDC+"\n")
			print("\t\t\t 2 - Nodes will use ground-auto selection firmware\n")
			print("\t\t\t 3 - Flash 'Blink' on every node\n")
			print("\t\t\t 4 - Flash each node individually\n")
			print("\t\t\t "+bcolors.YELLOW+"5 - Go back"+bcolors.ENDC+"\n")
			sleep(0.3)
			selection=str(raw_input(""))
			if selection=='1':
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_1.hex:i ")
				print("\n				Node 1 - flashed\n\n")
				sleep(1)
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_2.hex:i ")
				print("\n				Node 2 - flashed\n\n")
				sleep(1)
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_3.hex:i ")
				print("\n				Node 3 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_4.hex:i ")
				print("\n				Node 4 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_5.hex:i ")
				print("\n				Node 5 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_6.hex:i ")
				print("\n				Node 6 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_7.hex:i ")
				print("\n				Node 7 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_8.hex:i ")
				print("\n				Node 8 - flashed\n\n")
				sleep(1)
				logo2()
				sleep(2)
			if selection=='2':
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 1 - flashed\n\n")
				sleep(1)
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 2 - flashed\n\n")
				sleep(1)
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 3 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 4 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 5 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 6 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 7 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/node_0.hex:i ")
				print("\n				Node 8 - flashed\n\n")
				sleep(1)
				logo2()
				sleep(2)
			if selection=='3':
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 1 - flashed\n\n")
				sleep(1)
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 2 - flashed\n\n")
				sleep(1)
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 3 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 4 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 5 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 6 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 7 - flashed\n\n")
				sleep(1)
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600  -U flash:w:/home/"+user+"/RH-ota/firmware/blink.hex:i ")
				print("\n				Node 8 - flashed\n\n")
				sleep(1)
				logo2()
				sleep(2)
			if selection=='4':
				flashEachNode()
			if selection=='5':
				mainMenu()
			else:
				nodesUpdate()
			sleep(0.3)
		nodesUpdate()
		
	if selection=='3':
		def serverStart():
			os.system("clear")
			logo()
			#os.system("sudo pkill server.py")
			os.system("sudo systemctl stop rotorhazard")
			print("\n\n		Please wait...\n\n")
			print("\n")
			os.chdir("/home/"+user+"/RotorHazard/src/server/")
			os.system("python server.py")
		serverStart()
		
	if selection=='4':
		def featuresMenu():
			os.system("clear")
			logo()
			print("\n\n\n\t\t\t\t      "+bcolors.RED+"   FEATURES MENU\n"+bcolors.ENDC)
			print("\t\t\t   "+bcolors.BLUE+"1 - Install avrdude\n"+bcolors.ENDC)
			print("\t\t\t   "+bcolors.BLUE+"2 - Enable serial protocol"+bcolors.ENDC+"\n")
			print("\t\t\t   3 - Fix GPIO pins state\n")
			print("\t\t\t   4 - Raspberry as Access Point - coming soon\n")
			print("\t\t\t   5 - Useful aliases\n")
			print("\t\t\t   6 - Self updater - coming soon\n")
			print("\t\t\t   "+bcolors.YELLOW+"7 - Go back"+bcolors.ENDC)
			selection=str(raw_input(""))
			if selection=='1':
				def avrDude():
					os.system("clear")
					logo()
					print("\n\n\n						"+bcolors.RED+"AVRDUDE MENU"+bcolors.ENDC+"\n")
					print ("			 "+bcolors.BLUE+"1 - Install avrdude"+bcolors.ENDC)
					print ("			 2 - Check if nodes (at least one) are connected properly ")
					print ("			 "+bcolors.YELLOW+"3 - Go back"+bcolors.ENDC)
					selection=str(raw_input(""))
					if selection=='1' : 
						os.system("sudo apt-get update")
						os.system("sudo apt-get install avrdude")
					if selection=='2' : 
						os.system("sudo avrdude -c arduino -p m328p -v")
					if selection=='3' : 
						mainMenu()
				avrDude()
			if selection== '2':
				def serialEnable():
					os.system("echo 'enable_uart=1'| sudo  tee -a /boot/config.txt")
					os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
					print (" \t\t\t\tYou have to reboot Raspberry now. Ok?\n")
					print (" \t\t\t\t1 - Reboot now\n")
					print (" \t\t\t\t"+bcolors.YELLOW+"2 - Go back\n\n"+bcolors.ENDC)
					selection=str(raw_input(""))
					if selection=='1':
						os.system("sudo reboot")
					if selection== '2':
						featuresMenu()
					else:
						serialEnable()
				serialEnable()
			if selection=='3':
				def gpioState(): 
					os.system("clear")
					logo()
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
				gpioState()
			if selection=='4':
				def raspberryAP():
					print("coming soon")
					sleep(1)
			if selection=='5':
				def aliasesMenu():
					sleep(0.3)
					os.system("clear")
					sleep(0.3)
					def aliasesContent():
						os.system("echo '' | sudo tee -a ~/.bashrc")
						os.system("echo '### Shortcuts that can be used in terminal window ###' | sudo tee -a ~/.bashrc")
						os.system("echo '' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias ss=\"python ~/RotorHazard/src/server/server.py\"   #  starts the server' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias cfg=\"nano ~/RotorHazard/src/server/config.json\"   #  opens config.json file' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias rh=\"cd ~/RotorHazard/src/server\"   # goes to server file location' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias py=\"python\"  # pure laziness' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias sts=\"sudo systemctl stop rotorhazard\" # stops RH service' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias otadir=\"cd ~/RH-ota\"   # goes to server file location' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias ota=\"python ~/RH-ota/update.py\"  # opens updating script' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias als=\"nano ~/.bashrc\"   #  opens this file' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias rld=\"source ~/.bashrc\"   #  reloads aliases file' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias rcfg=\"sudo raspi-config\"   #  open raspberrys configs' | sudo tee -a ~/.bashrc")
						os.system("echo 'alias gitota=\"git clone https://github.com/szafranski/RH-ota.git\"   #  clones ota repo' | sudo tee -a ~/.bashrc")
						os.system("echo '' | sudo tee -a ~/.bashrc")
						os.system("echo '# After adding or changing aliases manually - reboot raspberry or type \"source ~/.bashrc\".' | sudo tee -a ~/.bashrc")
						os.system("echo 'leave this file here' | sudo tee -a ~/.aliases_added")
						os.system("source ~/.bashrc")
						print("\n\n\t\t	Aliases added successfully")
						sleep(2)
						featuresMenu()
					print("""\n\n\t\t
		Aliases in Linux act like shortcuts or referances to another commands. You can use them every time when you \n\t
		operates in the terminal window. For example instead of typing 'python ~/RotorHazard/src/server/server.py' \n\t
		you can just type 'ss' (server start) etc. Aliases can be modified and added anytime you want. You just \n\t  
		have to open '~./bashrc' file in text editor like 'nano'. After that you have reboot or type 'source ~/.bashrc' \n\t
		- or use alias 'rld'. \n\n\t
	       Alias			Command					What it does	\n
		ss 	-->  python ~/RotorHazard/src/server/server.py   # starts the server\n\t
		cfg 	-->  nano ~/RotorHazard/src/server/config.json   # opens config.json file\n\t
		rh  	-->  cd ~/RotorHazard/src/server   		 # goes to server file location\n\t
		py  	-->  python  					 # pure laziness\n\t
		sts  	-->  sudo systemctl stop rotorhazard 		 # stops RH service if was started\n\t
		otadir  -->  cd ~/RH-ota   				 # goes to main server file location\n\t
		ota  	-->  python ~/RH-ota/update.py  		 # opens updating script\n\t
		als  	-->  nano ~/.bashrc   				 # opens this file\n\t
		rld  	-->  source ~/.bashrc   			 # reloads aliases file \n\t
		rcfg  	-->  sudo raspi-config   			 # open raspberry's configs\n\t
		gitota	-->  git clone https://github.com/sza(...) 	 # clones ota repo\n\t\t\t\n
					Do you want to use above aliases in your system?
		""")
					
					selection=str(raw_input("\t\t\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
					if selection == 'y':
						if os.path.exists("/home/"+user+"/.aliases_added") == True:
							print("\n\n\t\t\t Looks like you already have aliases added. Do you want to continue anyway?\n")
							selection=str(raw_input("\t\t\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
							if selection=='y':
								aliasesContent()
							if selection =='a':
								featuresMenu()
							else:
								aliasesMenu()
						else:
							aliasesContent()
					if selection == 'a':
						featuresMenu()
					else:
						aliasesMenu()
				aliasesMenu()
			if selection=='6':
				print("coming soon")
				sleep(1)
			if selection=='7':
				mainMenu()
			else:
				featuresMenu()
		featuresMenu()
		
	if selection=='5':
		def firstTime():
			os.system("clear")
			sleep(0.3)
			print("""\n\n\n 
		More info here: https://www.instructables.com/id/RotorHazard-Updater/\n\n
		and in how_to folder - look for PDF file.\n\n 
			Enjoy!\n\
									Szafran\n\n """)
			selection=str(raw_input("\t\t\t\t\t"+bcolors.YELLOW+"Go back by pressing 'b'"+bcolors.ENDC+"\n"))
			if selection=='b':
				mainMenu()
			else :
				firstTime()
		firstTime()
	if selection=='6':
		def end():
			os.system("clear")
			print("\n\n")
			image()
			print("\n\t\t\t\t\t  Happy flyin'!\n")
			sleep(1.3)
			os.system("clear")
			sys.exit()
		end()
	else: 
		mainMenu()
mainMenu()

