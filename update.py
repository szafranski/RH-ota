####To do:####

# show 'flashed' - only after success
# define number of nodes

linux_testing = False  ### change to True for testing on Linux PC or WSL

######## Enter pins connected to reset pins on Arduino-nodes: ########

reset_1 = 12  ## node 1
reset_2 = 16  ## node 2
reset_3 = 20  ## node 3
reset_4 = 22  ## node 4
reset_5 = 6   ## node 5
reset_6 = 13  ## node 6
reset_7 = 19  ## node 7
reset_8 = 26  ## node 8


if (linux_testing == False):
	user = 'pi'   ## you can change it if your user is named differently

                                                                                


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

from PIL import Image

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
		allPinsLow()
		GPIO.output(reset_1, GPIO.HIGH)
	def nodeTwoReset():
		allPinsLow()
		GPIO.output(reset_2, GPIO.HIGH)
	def nodeThreeReset():
		allPinsLow()
		GPIO.output(reset_3, GPIO.HIGH)
	def nodeFourReset():
		allPinsLow()
		GPIO.output(reset_4, GPIO.HIGH)
	def nodeFiveReset():
		allPinsLow()
		GPIO.output(reset_5, GPIO.HIGH)
	def nodeSixReset():
		allPinsLow()
		GPIO.output(reset_6, GPIO.HIGH)
	def nodeSevenReset():
		allPinsLow()
		GPIO.output(reset_7, GPIO.HIGH)
	def nodeEightReset():
		allPinsLow()
		GPIO.output(reset_8, GPIO.HIGH)


if (linux_testing == True): 
	user='pfabi'   ### you can put here your username on the Linux PC - for testing
	def allPinsReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
	def allPinsLow():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
	def allPinsHigh():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeOneReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
			
	def nodeTwoReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeThreeReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeFourReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeFiveReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeSixReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeSevenReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)
		
	def nodeEightReset():
		print("\n\n\t\t\t\t\t Linux - PC\n\n")
		sleep(0.1)


def image():
	print("""
\t\t\t                               **/(((/**                              
\t\t\t                            */###########(*                           
\t\t\t                          */#####@@@@@#####(*                         
\t\t\t                         *(((((@@@###@@@#####*,                       
\t\t\t                       */((((@@@#######@@@####/*                      
\t\t\t                      *(((((@@@(((((#(##@@@#####*                     
\t\t\t                    **((((&@@&((((*...####@@@####**                   
\t\t\t                   *(((((@@@((((((....((((#@@@#####*                  
\t\t\t                 **((((#@@@((((((*.....((((#%@@&####/*                
\t\t\t                */((((@@@((((((((......(((((((@@@####(*               
\t\t\t              .*(((((@@@(((((((((......((((((((@@@%####**             
\t\t\t             */((((@@@(((((((((((......((((((((((@@@####(*            
\t\t\t            *(((((@@@((((((((((((.....*(((((((((((@@@#####*,          
\t\t\t          **((((@@@((((((((((((((.....((((((((((((((@@@(#(#/*         
\t\t\t          *((((@@@(((((((((((((((.....(((((((((((((((@@@((###*        
\t\t\t       */((((&@@&(((((((((((((,...(((....(((((((((((((#@@@((((/*      
\t\t\t      */((((@@@(((((((((......................((((((((((@@@((((#*     
\t\t\t    .*//(((@@@((((((............(((((((*.........,(((((((%@@&((((/*   
\t\t\t   */////@@@(((((........../((((((((((((((*..........((((((@@@(((((*  
\t\t\t  */////@@@/(((......./(((((((((((((((((((((((/......../((((@@@#((((*.
\t\t\t *////%@@/////(((((((((((((((((((((((((((((((((((((((..(((((((@@@((((*
\t\t\t *////@@@/////////((((((((((((((((((((((((((((((((((((((((((((@@@((((*
\t\t\t **/////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((**
\t\t\t  ***/////////////////(((((((((((((((((((((((((((((((((((((((((((((** 
\t\t\t     ****////////////////((((((((((((((((((((((((((((((((((((/****   
""")

def logo():
	os.system("clear")
	print("""\n\n	
		############################################################################################
		###                                                                                      ###
		###                                 """+bcolors.ORANGE+"""RotorHazard"""+bcolors.ENDC+"""                                          ###
		###                                                                                      ###
		###    You are about to flash nodes firmware. Please do not interrupt this operation!    ###
		###                                                                                      ###
		###                                                                                      ###
		############################################################################################""")



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
		print("\n\n\n\t\t\t\t\t\t "+bcolors.RED+"NODE MENU"+bcolors.ENDC)
		print("\n\t\t\t\t 1 - Flash node 1 \t\t 5 - Flash node 5")
		print("\n\t\t\t\t 2 - Flash node 2 \t\t 6 - Flash node 6")
		print("\n\t\t\t\t 3 - Flash node 3 \t\t 7 - Flash node 7")
		print("\n\t\t\t\t 4 - Flash node 4 \t\t 8 - Flash node 8")
		print("\n\t\t\t\t              9 - Back to main menu")
		selection=str(raw_input("\n\n\t\t\tWhich node do you want to program: "))
		print("\n\n")
		if selection=='1':
			print("\n\t\t\t\t Node 1 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_1.hex:i ")
			if selection=='2' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='2':
			print("\n\\t\t\t\t Node 2 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_2.hex:i ")
			if selection=='2' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='3':
			print("\n\t\t\t\t Node 3 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_3.hex:i ")
			if selection=='2' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='4':
			print("\n\t\t\t\t Node 4 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_4.hex:i ")
			if selection=='2' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='5':
			print("\n\t\t\t\t Node 5 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_5.hex:i ")
			if selection=='2' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeFiveReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='6':
			print("\n\t\t\t\t Node 6 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_6.hex:i ")
			if selection=='2' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeSixReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='7':
			print("\n\t\t\t\t Node 7 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_7.hex:i ")
			if selection=='2' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeSevenReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			print("\n\t Node flashed")
			if selection=='4':
				nodeMenu()
			nodeMenu()
		if selection=='8':
			print("\n\t\t\t\t Node 8 selected")
			print("\n\n\t\t\t Choose flashing type\n")
			print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
			print("\t\t\t 2 - Node ground-auto selection firmware")
			print("\t\t\t 3 - Flashes 'Blink' on the node")
			print("\t\t\t 4 - Abort")
			selection=str(raw_input(""))
			if selection=='1' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_8.hex:i ")
			if selection=='2' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i")
			if selection=='3' : 
				nodeEightReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
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
	print("\n\n\n\t\t\t\t\t\t "+bcolors.RED+"MAIN MENU\n"+bcolors.ENDC)
	print("\t\t\t\t\t "+bcolors.BLUE+"1 - Server software installation and update\n	"+bcolors.ENDC)
	print("\t\t\t\t\t "+bcolors.BLUE+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("\t\t\t\t\t 3 - Start the server now\n")
	print("\t\t\t\t\t 4 - Additional features\n")
	print("\t\t\t\t\t 5 - This is my first time - READ!\n")
	print("\t\t\t\t\t 6 - Exit")
	selection=str(raw_input(""))
	if selection=='1':
		sleep(0.1)
		os.system('python ./rpi_soft.py')
	if selection=='2':
		def nodesUpdate():
			os.system("clear")
			logo()
			print("\n\n\t\t\t\t Choose flashing type\n")
			print("\t\t\t "+bcolors.GREEN+"1 - Every Node gets own dedicated firmware - recommended"+ bcolors.ENDC)
			print("\t\t\t 2 - Nodes will use ground-auto selection firmware")
			print("\t\t\t 3 - Flash 'Blink' on every node")
			print("\t\t\t 4 - Flash each node individually")
			print("\t\t\t 5 - Go back")
			sleep(0.1)
			selection=str(raw_input(""))
			if selection=='1':
				programming_type = 1
			if selection=='2':
				programming_type = 2	
			if selection=='3':
				programming_type = 3
			if selection=='4':
				flashEachNode()
			if selection=='5':
				mainMenu()
			else:
				nodesUpdate()
				
			os.system("sudo pkill server.py")
			os.system("sudo systemctl stop rotorhazard")

			if programming_type ==1 : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_1.hex:i ")
			if programming_type ==2 : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeOneReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 1 - flashed")
			print("\n\n")
			sleep(0.2)

			if programming_type ==1 : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_2.hex:i ")
			if programming_type ==2 : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeTwoReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 2 - flashed")
			print("\n\n")
			sleep(0.2)

			if programming_type ==1 : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_3.hex:i ")
			if programming_type ==2 : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeThreeReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 3 - flashed")
			print("\n\n")
			sleep(0.2)

			if programming_type ==1 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_4.hex:i ")
			if programming_type ==2 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 4 - flashed")
			print("\n\n")
			sleep(0.2)

			if programming_type ==1 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_5.hex:i ")
			if programming_type ==2 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 5 - flashed")
			print("\n\n")

			if programming_type ==1 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_6.hex:i ")
			if programming_type ==2 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 6 - flashed")
			print("\n\n")

			if programming_type ==1 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_7.hex:i ")
			if programming_type ==2 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 7 - flashed")
			print("\n\n")

			if programming_type ==1 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_8.hex:i ")
			if programming_type ==2 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/node_0.hex:i ")
			if programming_type ==3 : 
				nodeFourReset()
				os.system("sudo avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH-ota/firmware/blink.hex:i ")
			sleep(0.1)

			print("")
			print("				Node 8 - flashed")
			print("\n\n")	
			
			sleep(0.1)
			print("""
				##########################################################################################
				###                                                                                    ###
				###             CONGRATULATIONS!            Flashing firmware to nodes - DONE          ###
				###                                                                                    ###
				###                                                                                    ###
				###    Please power off the timer, unplug voltage source for few seconds and reboot    ###
				###                                                                                    ###
				##########################################################################################
			\n\n""")
			sleep(3)
		nodesUpdate()

	if selection=='3':
		def serverStart():
			os.system("clear")
			logo()
			os.system("sudo pkill server.py")
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
			print("\n\n\n\t\t\t\t\t\t "+bcolors.RED+"FEATURES MENU\n"+bcolors.ENDC)
			print("\t\t\t\t\t 1 - Install avrdude\n")
			print("\t\t\t\t\t 2 - Enable serial protocol\n")
			print("\t\t\t\t\t 3 - Fix GPIO pins state\n")
			print("\t\t\t\t\t 4 - Raspberry as Access Point - coming soon\n")
			print("\t\t\t\t\t 5 - Useful aliases - coming soon\n")
			print("\t\t\t\t\t 6 - Go back")
			selection=str(raw_input(""))
			if selection=='1':
				def avrDude():
					os.system("clear")
					logo()
					print("\n\n\n						"+bcolors.RED+"AVRDUDE MENU"+bcolors.ENDC+"\n")
					print ("			 "+bcolors.BLUE+"1 - Install avrdude"+bcolors.ENDC)
					print ("			 2 - Check if nodes (at least one) are connected properly ")
					print ("			 3 - Go back")
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
					os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
					print (" \t\t\t\tYou have to reboot Raspberry now. Ok?\n")
					print (" \t\t\t\t1 - Reboot now\n")
					print (" \t\t\t\t2 - Go back\n\n")
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

			if selection=='5':
				def aliases():
					print("coming soon")
			if selection=='6':
				mainMenu()
			else:
				featuresMenu()
		featuresMenu()
		
	if selection=='5':
		def firstTime():
			os.system("clear")
			sleep(0.1)
			print("""\n\n\n 
			Hello - tutorial - coming soon
			
				Enjoy!\n\
												Szafran\n\n """)
			selection=str(raw_input("\t\t\t\t\t"+bcolors.YELLOW+"Go back by pressing 'b'"+bcolors.ENDC+"\n"))
			if selection=='b':
				mainMenu()
			else :
				firstTime()
	if selection=='6':
		def end():
			os.system("clear")
			print("\n\n")
			image()
			print("\n\t\t\t\t\t\t  Happy flyin'!\n")
			sleep(1.3)
			os.system("clear")
			sys.exit()
		end()
	else: 
		mainMenu()
mainMenu()


