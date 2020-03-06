####To do:####
# avrdude test
# Access Point

from time import sleep
import os
import sys
import json

updater_version = '2.2.6d'   ### version of THIS program - has nothing to do with the RH version
                            ### it reffers to the API level of newest contained nodes firmware 
                            ### third number reffers to actual verion of the updater itself

homedir = os.path.expanduser('~')

if os.path.exists(homedir+"/RH-ota/updater-config.json") == True:
	with open('updater-config.json') as config_file:
		data = json.load(config_file)
else:
	with open('distr-updater-config.json') as config_file:
		data = json.load(config_file)

preffered_RH_version = data['RH_version']

if preffered_RH_version == 'master':
	firmware_version = 'master'
if preffered_RH_version == 'beta':
	firmware_version = 'beta'
if preffered_RH_version == 'stable':
	firmware_version = 'stable'
if preffered_RH_version == 'custom':
	firmware_version = 'stable'

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

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
		print("\t\t\t  Linux PC version\t")
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

def compatibility():               ### adds compatibility with previous versions
	if os.path.exists(homedir+"/.ota_markers") == False:
		os.system("mkdir "+homedir+"/.ota_markers")
	if os.path.exists(homedir+"/.aliases_added") == True:
		if os.path.exists(homedir+"/.ota_markers/.aliases_added") == False:
			os.system("cp "+homedir+"/.aliases_added "+homedir+"/.ota_markers/.aliases_added ")
		os.system("rm "+homedir+"/.aliases_added")
	if os.path.exists(homedir+"/.updater_self") == True:
		if os.path.exists(homedir+"/.ota_markers/.aliases_added") == False:
			os.system("cp "+homedir+"/.updater_self "+homedir+"/.ota_markers/.updater_self ")
		os.system("rm "+homedir+"/.updater_self")
	if os.path.exists(homedir+"/.old_RotorHazard.old/.installation-check_file.txt") == True:
		if os.path.exists(homedir+"/.ota_markers/.installation-check_file.txt") == False:
			os.system("cp /home/"+user+"/.old_RotorHazard.old/.installation-check_file.txt "+homedir+"/.ota_markers/.installation-check_file.txt")
		os.system("rm "+homedir+"/.installation-check_file.txt")
	if os.path.exists(homedir+"/.serialok") == True:
		if os.path.exists(homedir+"/.ota_markers/.serialok") == False:
			os.system("cp "+homedir+"/.serialok "+homedir+"/.ota_markers/.serialok")
		os.system("rm "+homedir+"/.serialok")
	if os.path.exists(homedir+"/.bashrc") == True:
		if check_if_string_in_file(homedir+'/.bashrc', 'RotorHazard OTA Manager updated'):
			os.system("sed -i 's/alias updateupdater/# alias updateupdater/g' "+homedir+"/.bashrc")
			os.system("""echo 'alias updateupdater=\"cd ~ && sudo cp ~/RH-ota/self.py ~/.ota_markers/self.py && sudo python ~/.ota_markers/self.py \"  # part of self-updater' | sudo tee -a ~/.bashrc""")

def first ():
	image ()
	if linux_testing == False:
		os.system("sudo systemctl stop rotorhazard")
	os.system("clear")
	print("\n\n")
	image()
	print("\t\t\t\t\t Updater version: "+str(updater_version))
	compatibility()
	sleep(1.1)
first()

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
			mainMenu()
		else:
			nodeMenu()
	nodeMenu()

def avrDude():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\n\t\t\t\t\t\t"+bcolors.RED+"AVRDUDE MENU"+bcolors.ENDC+"\n")
	print ("\t\t\t "+bcolors.BLUE+"1 - Install avrdude"+bcolors.ENDC)
	print ("\t\t\t "+bcolors.YELLOW+"2 - Go back"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1' : 
		os.system("sudo apt-get update")
		os.system("sudo apt-get install avrdude -y")
	if selection=='2' : 
		mainMenu()

def serialMenu():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	def serialContent():
		os.system("echo 'functionality added' | sudo tee -a ~/.ota_markers/.serialok")
		os.system("echo 'enable_uart=1'| sudo  tee -a /boot/config.txt")
		os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
		print("\n\n\t\t\t	Serial port enabled successfully")
		print (" \n\t\t\t\tYou have to reboot Raspberry now. Ok?\n")
		print (" \t\t\t\t\t'r' - Reboot now\n")
		print (" \t\t\t\t\t"+bcolors.YELLOW+"'b' - Go back\n\n"+bcolors.ENDC)
		selection=str(raw_input(""))
		if selection=='r':
			os.system("sudo reboot")
		if selection== 'b':
			featuresMenu()
	print("""\n\n\t\tSerial port has to be enabled. Without it Arduinos cannot be programmed.
			\n\t\tDo you want to enable it now?""")
	selection=str(raw_input("\n\t\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		if os.path.exists("/home/"+user+"/.ota_markers/.serialok") == True:
			print("\n\n\t\t Looks like you already enabled Serial port. Do you want to continue anyway?\n")
			selection=str(raw_input("\t\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
			if selection=='y':
				serialContent()
			if selection =='a':
				featuresMenu()
			else:
				serialMenu()
		else:
			serialContent()
	if selection == 'a':
		featuresMenu()
	else:
		serialMenu()

def aliasesMenu():
	sleep(0.2)
	os.system("clear")
	sleep(0.2)
	def aliasesContent():
		os.system("echo '' | sudo tee -a ~/.bashrc")
		os.system("echo '### Shortcuts that can be used in terminal window ###' | sudo tee -a ~/.bashrc")
		os.system("echo '' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias ss=\"cd ~/RotorHazard/src/server && python server.py\"   #  starts the server' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias cfg=\"nano ~/RotorHazard/src/server/config.json\"   #  opens config.json file' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias rh=\"cd ~/RotorHazard/src/server\"   # goes to server file location' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias py=\"python\"  # pure laziness' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias sts=\"sudo systemctl stop rotorhazard\" # stops RH service' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias otadir=\"cd ~/RH-ota\"   # goes to server file location' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias ota=\"cd ~/RH-ota && python update.py\"  # opens updating script' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias als=\"nano ~/.bashrc\"   #  opens this file' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias rld=\"source ~/.bashrc\"   #  reloads aliases file' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias rcfg=\"sudo raspi-config\"   #  open raspberrys configs' | sudo tee -a ~/.bashrc")
		os.system("echo 'alias gitota=\"git clone --depth=1 https://github.com/szafranski/RH-ota.git\"   #  clones ota repo' | sudo tee -a ~/.bashrc")
		os.system("echo '' | sudo tee -a ~/.bashrc")
		os.system("echo '# After adding or changing aliases manually - reboot raspberry or type \"source ~/.bashrc\".' | sudo tee -a ~/.bashrc")
		os.system("echo 'functionality added' | sudo tee -a ~/.ota_markers/.aliases_added")
		print("\n\n\t\t	Aliases added successfully")
		sleep(2)
		featuresMenu()
	print("""\n\n\t\t
	Aliases in Linux act like shortcuts or referances to another commands. You can use them every time when you \n\t
	operates in the terminal window. For example instead of typing 'python ~/RotorHazard/src/server/server.py' \n\t
	you can just type 'ss' (server start) etc. Aliases can be modified and added anytime you want. You just \n\t  
	have to open '~./bashrc' file in text editor like 'nano'. After that you have reboot or type 'source ~/.bashrc'. \n\n\t
	Alias			Command					  What it does	\n
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
		Do you want to use above aliases in your system?""")
	selection=str(raw_input("\n\t\t\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		if os.path.exists("/home/"+user+"/.ota_markers/.aliases_added") == True:
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

def selfUpdater():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	if os.path.exists("/home/"+user+"/.ota_markers/.updater_self") == True:
		print("""\n\n 
		If you want to update this program and download new firmware, \n
		prepared for Arduino nodes - so you can next flash them \n\t\t
		- you have to type 'updateupdater' in the terminal window.\n\n\t\t
		Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+""",\n\t\t
		so you allways know what firmware version updater contains.\n\t\t
		For example "2.2.3" contains nodes firmware with "API level 22" etc.\n\t\t
		Be sure that you have internet connection established.\n\n """)
		print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Exit program by pressing 'e' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
		+bcolors.YELLOW+"""\tGo back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
		selection=str(raw_input(""))
		if selection=='e':
			sys.exit()
		if selection=='b':
			featuresMenu()
		else :
			selfUpdater()
	else:
		os.system("""echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self-updater' | sudo tee -a ~/.bashrc""")
		sleep(0.1)
		os.system("echo 'updater marker' | sudo tee -a ~/.ota_markers/.updater_self")
		sleep(0.12)
		os.system("clear")
		sleep(0.12)
		logoTop()
		sleep(0.12)
		print("""\n\n 
		If you want to update this program and download new firmware, \n
		prepared for Arduino nodes - so you can next flash them  \n\t\t
		- you have to reboot the Raspberry. Next step is to type  \n\t\t
		'updateupdater' in the terminal window.\n\t\t
		Next time you won't have to reboot before updating.\n\n\t\t
		Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+""",\n\t\t
		so you allways know what firmware version updater contains.\n\t\t
		For example 2.2.1 contains nodes firmware with API 22 etc.\n\t\t
		Be sure that you have internet connection established.\n\n """)
		print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
		+bcolors.YELLOW+"""\tGo back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
		selection=str(raw_input(""))
		if selection=='r':
			os.system("sudo reboot")
		if selection=='b':
			featuresMenu()
		else :
			selfUpdater()

def featuresMenu():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\n\t\t\t\t\t\t"+bcolors.RED+"FEATURES MENU\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"1 - Install avrdude\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"2 - Enable serial protocol"+bcolors.ENDC+"\n")
	print("\t\t\t   3 - Access Point and Internet - coming soon\n")
	print("\t\t\t   4 - Useful aliases\n")
	print("\t\t\t   5 - Self updater \n")
	print("\t\t\t   "+bcolors.YELLOW+"6 - Go back"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1':
		avrDude()
	if selection== '2':
		serialMenu()
	if selection=='3':
		def raspberryAP():   ### in development
			if linux_testing == True:
				os.system("python ./net_and_ap.py")
			else:
				os.system("clear")
				print("\n\n\n\t\t\t\tcoming soon")
				sleep(1.5)
		raspberryAP()
	if selection=='4':
		aliasesMenu()
	if selection=='5':
		selfUpdater()
	if selection=='6':
		mainMenu()
	else:
		featuresMenu()

def serverStart():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	print("\n\n\t\tPlease wait...\n\n")
	print("\n")
	os.system("python server.py")
	os.chdir("/home/"+user+"/RotorHazard/src/server")

def firstTime():
	def secondPage():
		sleep(0.12)
		os.system("clear")
		sleep(0.12)
		print("""\n\n 
		\t\t\tCONFIGURATION FILE:\n\n
		Copy "distr-updater-config.json" from same folder to "updater-config.json". \n
		Use: 'cp distr-updater-config.json updater-config.json'.\n
		Next, edit new file using 'nano' command, make changes and save. \n\n
		Possible RotorHazard versions:\n
		> """+bcolors.BLUE+"""\"stable\""""+bcolors.ENDC+""" - last stable release (can be from before few months)\n
		> """+bcolors.BLUE+"""\"beta\""""+bcolors.ENDC+"""   - last beta release (usually few weeks, quite stable)\n
		> """+bcolors.BLUE+"""\"master\""""+bcolors.ENDC+""" - absolutely newest release (even if not well tested)\n
		""")
		selection=str(raw_input("\n\t\t\t"+bcolors.GREEN+"'f' - first page'"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - back to menu"+bcolors.ENDC+"\n"))
		if selection=='f':
			firstPage()
		if selection=='b':
			mainMenu()
		else :
			secondPage()
	def firstPage():
		sleep(0.12)
		os.system("clear")
		sleep(0.12)
		print("""\n\n\n 
		You can use all implemened features, but if you want to be able to program\n
		Arduino-based nodes - enter Features menu and begin with first 2 points.\n\n
		Also remember about setting up config file - check second page.  \n\n
		More info here: https://www.instructables.com/id/RotorHazard-Updater/\n
		and in how_to folder - look for PDF file.\n\n 
		\t\n\t\t\tEnjoy!\n\t\t\t\t\t\t\t\tSzafran\n\n\n """)
		selection=str(raw_input("\t\t\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
		if selection=='s':
			secondPage()
		if selection=='b':
			mainMenu()
		else :
			firstPage()
	firstPage()

def end():
		os.system("clear")
		print("\n\n")
		image()
		print("\t\t\t\t\t  Happy flyin'!\n")
		sleep(1.3)
		os.system("clear")
		sys.exit()

def mainMenu():
	sleep(0.12)
	os.system("clear")
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\n\t\t\t\t\t "+bcolors.RED+"   MAIN MENU\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"1 - Server software installation and update\n	"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("\t\t\t   3 - Start the server now\n")
	print("\t\t\t   4 - Additional features\n")
	print("\t\t\t   5 - This is my first time - READ!\n")
	print("\t\t\t   "+bcolors.YELLOW+"6 - Exit"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1':
		os.system("python ./rpi_update.py")   ### opens raspberry updating file
	if selection=='2':
		os.system("python ./nodes_update.py")   ### opens nodes updating file
	if selection=='3':
		serverStart()
	if selection=='4':
		featuresMenu()
	if selection=='5':
		firstTime()
	if selection=='6':
		end()
	else: 
		mainMenu()
mainMenu()

