####To do:####

# show 'flashed' - only after success

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
		GPIO.output(reset_1, GPIO.LOW)
		GPIO.output(reset_2, GPIO.LOW)
		GPIO.output(reset_3, GPIO.LOW)
		GPIO.output(reset_4, GPIO.LOW)
		GPIO.output(reset_5, GPIO.LOW)
		GPIO.output(reset_6, GPIO.LOW)
		GPIO.output(reset_7, GPIO.LOW)
		GPIO.output(reset_8, GPIO.LOW)	
		sleep(0.1)

def nodeOneReset():
	GPIO.output(reset_1, GPIO.LOW)
	sleep(0.05)
	GPIO.output(reset_1, GPIO.HIGH)
		
def nodeTwoReset():
	GPIO.output(reset_2, GPIO.LOW)
	sleep(0.05)
	GPIO.output(reset_2, GPIO.HIGH)
	
def nodeThreeReset():
	GPIO.output(reset_3, GPIO.LOW)
	sleep(0.05)
	GPIO.output(reset_3, GPIO.HIGH)
	
def nodeFourReset():
	GPIO.output(reset_4, GPIO.LOW)
	sleep(0.05)
	GPIO.output(reset_4, GPIO.HIGH)
	
def nodeFiveReset():
	GPIO.output(reset_5, GPIO.LOW)
	GPIO.output(reset_5, GPIO.HIGH)
	
def nodeSixReset():
	GPIO.output(reset_6, GPIO.LOW)
	GPIO.output(reset_6, GPIO.HIGH)
	
def nodeSevenReset():
	GPIO.output(reset_7, GPIO.LOW)
	GPIO.output(reset_7, GPIO.HIGH)
	
def nodeEightReset():
	GPIO.output(reset_8, GPIO.LOW)
	GPIO.output(reset_8, GPIO.HIGH)
		
		
if (linux_testing == True): 
	user='pfabi'   ### you can put here your username on the Linux PC - for testing
	def allPinsReset():
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
	sleep(1.6)
first()

def mainMenu():
	os.system("clear")
	logo()

	print("\n\n\n\t\t\t\t\t\t "+bcolors.RED+"MAIN MENU\n"+bcolors.ENDC)
	print("\t\t\t\t\t 1 - Nodes flash and update")
	print("\t\t\t\t\t 2 - Advanced menu")
	print("\t\t\t\t\t 3 - Exit")
	print("\t\t\t\t\t 4 - This is my first time - READ!")
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
	os.system("clear")
	logo()
	print("\n\n\t\t\t\t Choose flashing type\n")
	print("\t\t\t "+bcolors.GREEN+"1 - Every Node gets own dedicated firmware - recommended"+ bcolors.ENDC)
	print("\t\t\t 2 - Nodes will use ground-auto selection firmware")
	print("\t\t\t 3 - Flash 'blank' hex on every node")
	print("\t\t\t 4 - Go back")
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

	if programming_type ==1 : 
		nodeOneReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_1_wb.hex:i ")
	if programming_type ==2 : 
		nodeOneReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_0_wb.hex:i ")
	if programming_type ==3 : 
		nodeOneReset()
		os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.1)

	print("")
	print("				Node 1 - flashed")
	print("\n\n")
	sleep(0.2)

	if programming_type ==1 : 
		nodeTwoReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_2_wb.hex:i ")
	if programming_type ==2 : 
		nodeTwoReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_0_wb.hex:i ")
	if programming_type ==3 : 
		nodeTwoReset()
		os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.1)

	print("")
	print("				Node 2 - flashed")
	print("\n\n")
	sleep(0.2)

	if programming_type ==1 : 
		nodeThreeReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_3_wb.hex:i ")
	if programming_type ==2 : 
		nodeThreeReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_0_wb.hex:i ")
	if programming_type ==3 : 
		nodeThreeReset()
		os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.1)

	print("")
	print("				Node 3 - flashed")
	print("\n\n")
	sleep(0.2)

	if programming_type ==1 : 
		nodeFourReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_4_wb.hex:i ")
	if programming_type ==2 : 
		nodeFourReset()
		os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_0_wb.hex:i ")
	if programming_type ==3 : 
		nodeFourReset()
		os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.1)

	print("")
	print("				Node 4 - flashed")
	print("\n\n")
	sleep(0.2)

	os.system("sudo sed -i 's/reset .*/reset = "+str(reset_5)+";/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_5.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 5 - flashed")
	print("\n\n")

	os.system("sudo sed -i 's/reset .*/reset = "+str(reset_6)+";/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_6.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 6 - flashed")
	print("\n\n")

	os.system("sudo sed -i 's/reset .*/reset = "+str(reset_7)+";/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_7.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

	print("")
	print("				Node 7 - flashed")
	print("\n\n")

	os.system("sudo sed -i 's/reset .*/reset = "+str(reset_8)+";/g' /root/.avrduderc")
	if programming_type ==1 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_8.hex:i")
	if programming_type ==2 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
	if programming_type ==3 : os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
	sleep(0.3)

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
	sleep(5)
def exit():
	os.system("clear")
	print("\n\n")
	image()
	print("\n\t\t\t\t\t\t  Happy flyin'!\n")
	sleep(1.3)
	os.system("clear")
	sys.exit()
def advanced():
	os.system("clear")
	logo()
	def advancedMenu():
		print("\n\n")
		print("\t\t\t			"+bcolors.RED+"ADVANCED MENU:\n"+bcolors.ENDC)
		print("\t\t\t		 1 - Flash the bootloader")
		print("\t\t\t		 2 - Fix GPIO pins state")
		print("\t\t\t		 3 - Try to recover nodes")
		print("\t\t\t		 4 - Start the server now")
		print("\t\t\t		 "+bcolors.BLUE+"5 - Install / check avrdude"+bcolors.ENDC)
		print("\t\t\t		 6 - Program specific node")
		print("\t\t\t		 7 - Back to main menu")
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
			mainMenu()
		else:
			advanced()
	def bootloader(): 
		os.system("clear")
		logo()
		print("\n\n\t\t\t\t\t\t "+ bcolors.RED+"BOOTLOADER MENU"+ bcolors.ENDC)
		print("\n\t\t 1 - Flash the bootloader on node \t\t 5 - Flash the bootloader on node 5")
		print("\n\t\t 2 - Flash the bootloader on node \t\t 6 - Flash the bootloader on node 6")
		print("\n\t\t 3 - Flash the bootloader on node \t\t 7 - Flash the bootloader on node 7")
		print("\n\t\t 4 - Flash the bootloader on node \t\t 8 - Flash the bootloader on node 8")
		print("\n\t\t                                  9 - Go back")
		print("\n\n\t\t\t\t\t\t\t * after flashing the bootloader on a given node")
		print("\n\t\t\t\t\t\t\t   remove that node from the laptimer is you want to flash ")
		print("\n\t\t\t\t\t\t\t   anything on any different node")
		selection=str(raw_input("\n\n\t\t\tWhich node do you want to flash bootloader on: "))
		print("\n\n\n\n")
		if selection=='1':
			print("\n\t Node 1 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_1)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='2':
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_2)+";/g' /root/.avrduderc")
			print("\n\t Node 2 selected")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='3':
			print("\n\t Node 3 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_3)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='4':
			print("\n\t Node 4 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_4)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='5':
			print("\n\t Node 5 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_5)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='6':
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_6)+";/g' /root/.avrduderc")
			print("\n\t Node 6 selected")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='7':
			print("\n\t Node 7 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_7)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")
		if selection=='8':
			print("\n\t Node 8 selected")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_8)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.b.hex:i")
			print("\n\t Bootloader flashed")			
		if selection=='9':
			advanced()
		bootloader()
	def gpio_fix(): 
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
		advanced()
	def recover():
		os.system("clear")
		logo()
		print("\n\n\n\t 		Attempting recovery...\n\n")
		sleep(0.2)
		x = 1
		while x <= 2:
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_1)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_2)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_3)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_4)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_5)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_6)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_7)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			os.system("sudo sed -i 's/reset .*/reset = "+str(reset_8)+";/g' /root/.avrduderc")
			os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:blank.hex:i")
			sleep(0.7)
			x += 1
		print("\n\n		DONE\n\n")
		sleep(0.8)
		advanced()
	def server_start():
		os.system("clear")
		logo()
		print("\n\n\t   Server will start in 5 seconds\n\n")
		print("\n\n		Please wait...\n\n")
		print("\n")
		sleep(4) # time for all Arduinos to boot 
		os.system("sudo pkill server.py")
		os.system("sudo systemctl stop rotorhazard")
		os.chdir("/home/"+user+"/RotorHazard/src/server/")
		os.system("python server.py")
	def avr_info():
		os.system("clear")
		logo()
		print("\n\n\n						"+bcolors.RED+"AVRDUDE MENU"+bcolors.ENDC+"\n")
		print ("			 1 - Check the state of avrdude installation + config file")
		print ("			 2 - Check if nodes (at least one) are connected properly ")
		print ("			 "+bcolors.BLUE+"3 - Install avrdude"+bcolors.ENDC)
		print ("			 4 - Go back")
		selection=str(raw_input(""))
		if selection=='1' : 
			os.system("sudo avrdude -v")
		if selection=='2' : 
			os.system("sudo avrdude -c arduino -p m328p -v")
		if selection=='3' : 
			os.system("sudo apt-get update")
			os.system("sudo apt-get install avrdude")
			os.chdir("/home/"+user)
		if selection=='4' : 
			advanced()
		avr_info()
	def program_node():
		def nodeMenu():
			os.system("clear")
			logo()
			print("\n\n\n\t\t\t\t\t\t "+bcolors.RED+"NODE MENU"+bcolors.ENDC)
			print("\n\t\t\t\t 1 - Flash node 1 \t\t 5 - Flash node 5")
			print("\n\t\t\t\t 2 - Flash node 2 \t\t 6 - Flash node 6")
			print("\n\t\t\t\t 3 - Flash node 3 \t\t 7 - Flash node 7")
			print("\n\t\t\t\t 4 - Flash node 4 \t\t 8 - Flash node 8")
			print("\n\t\t\t\t                   9 - Go back")
			selection=str(raw_input("\n\n\t\t\tWhich node do you want to program: "))
			print("\n\n")
			if selection=='1':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_1)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 1 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeOneReset()
					os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_1_wb.hex:i ")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='2':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_2)+";/g' /root/.avrduderc")
				print("\n\\t\t\t\t Node 2 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeTwoReset()
					os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_2_wb.hex:i ")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='3':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_3)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 3 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeThreeReset()
					os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_3_wb.hex:i ")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='4':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_4)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 4 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					nodeFourReset()
					os.system("avrdude -v -p atmega328p -c arduino -P /dev/ttyS0 -b 57600 -D -U flash:w:/home/pi/RH_ota/firmware/node_4_wb.hex:i ")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='5':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_5)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 5 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_5.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='6':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_6)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 6 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_6.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='7':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_7)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 7 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='8':
				os.system("sudo sed -i 's/reset .*/reset = "+str(reset_8)+";/g' /root/.avrduderc")
				print("\n\t\t\t\t Node 8 selected")
				print("\n\n\t\t\t Choose flashing type\n")
				print("\t\t\t 1 - "+bcolors.GREEN+"Node gets own dedicated firmware - recommended"+bcolors.ENDC)
				print("\t\t\t 2 - Node ground-auto selection firmware")
				print("\t\t\t 3 - Flashes 'blank' hex on the node")
				print("\t\t\t 4 - Abort")
				selection=str(raw_input(""))
				if selection=='1' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota_4.hex:i")
				if selection=='2' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/node_ota.hex:i")
				if selection=='3' : 
					os.system("sudo avrdude -c linuxgpio -p m328p -v -U flash:w:firmware/blank.hex:i")
				print("\n\t Node flashed")
				if selection=='4':
					nodeMenu()
			if selection=='9':
				advanced()
		nodeMenu()
	advancedMenu()

def first():
	os.system("clear")
	sleep(0.1)
	print("""\n\n\n 
	 Hello! You are using tool designed to easy uploadig the firmware on the RotorHazard race-timer nodes.\n\t
	 For now consider this tool as a beta verision. Tests are being done constantly.\n
	
	 Files that you are about to flash are 'hex' files from an official RotorHazard Arduino nodes ino files.\n\t
	 After using this tool nodes would be flashed WITHOUT the bootloader which means,\n\t
	 that you won't be able to connect your Arduinos to the usb port and using it with PC anymore,\n\t
	 unless you flash bootloader back using 'Advanced menu' of this software.\n\t
	
	 It is recommended to flash nodes with specfic file for every node, even if you did auto selection mod.\n\t
	 This way you can allways check if nodes were flashed and recognized correctly during manual boot \n\t
	 of the server file - what smartass as you would do after flashing new firmware anyways. :) \n\t
	
	 If you are using this tool for the first time enter 'Advanced menu' and select 'Install avrdude'.\n\t
	 For more hardware instructions open 'manuals' file or visit Facebook page.\n\t
	
		Enjoy!\n\
										Szafran\n\n """)
	selection=str(raw_input("\t\t\t\t\t"+bcolors.YELLOW+"Go back by pressing 'b'"+bcolors.ENDC+"\n"))
	if selection=='b':
		mainMenu()
	else :
		first()
mainMenu()


