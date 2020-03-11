####To do:####
# avrdude test - maybe

from time import sleep
import os
import platform
import sys
import json
import subprocess

updater_version = '2.2.9d'  ### version of THIS program - has nothing to do with the RH version
                            ### it reffers to the API level of newest contained nodes firmware 
                            ### third number reffers to actual verion of the updater itself

homedir = os.path.expanduser('~')

#rldals = subprocess.Popen(["/bin/bash", "-i", "-c", "source ~/.bashrc"])

if os.path.exists("./updater-config.json") == True:
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

def clearTheScreen():
	sleep(0.05)
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")
	sleep(0.05)

def image():
	with open('image.txt', 'r') as file:
		f = file.read()
		print(f)

def logoTop():
	print("""\n	
	#######################################################################
	###                                                                 ###
	###\t\t\t"""+bcolors.ORANGE+"""     """+bcolors.BOLD+"""RotorHazard        """+bcolors.ENDC+"""\t\t    ###
	###                                                                 ###
	###                     """+bcolors.BOLD+"""OTA Updater and Manager"""+bcolors.ENDC+"""                     ###
	###                                                                 ###
	#######################################################################""")
	if (linux_testing == True):
		print("\t\t\t  Linux PC version\t\n")
	if os.path.exists("./updater-config.json") == False:
		print("""\t\tLooks that you haven't set up config file yet.
		Please read about configuration process - point 5
		and next enter configuration wizard - point 6.""")
	sleep(0.05)

def compatibility():               ### adds compatibility and fixes with previous versions
	os.system("python ./prev_comp.py")

#		if check_if_string_in_file(homedir+'/.bashrc', 'rld'):
#			rldals.communicate()

def first ():
	compatibility()
	clearTheScreen()
	print("\n\n")
	image()
	print("\t\t\t\t Updater version: "+str(updater_version))
	sleep(1.1)
first()

def avrDude():
	clearTheScreen()
	logoTop()
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
	clearTheScreen()
	logoTop()
	def serialContent():
		os.system("echo 'functionality added' | tee -a ~/.ota_markers/.serialok")
		os.system("echo 'enable_uart=1'| sudo tee -a /boot/config.txt")
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
	selection=str(raw_input("\n\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		if os.path.exists("/home/"+user+"/.ota_markers/.serialok") == True:
			print("\n\n\t\tLooks like you already enabled Serial port. Do you want to continue anyway?\n")
			selection=str(raw_input("\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
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
	clearTheScreen()
	def aliasesContent():
		os.system("echo '' | tee -a ~/.bashrc")
		os.system("echo '### Shortcuts that can be used in terminal window ###' | tee -a ~/.bashrc")
		os.system("echo '' | tee -a ~/.bashrc")
		os.system("echo 'alias ss=\"cd ~/RotorHazard/src/server && python server.py\"   #  starts the RH-server' | tee -a ~/.bashrc")
		os.system("echo 'alias cfg=\"nano ~/RotorHazard/src/server/config.json\"   #  opens config.json file' | tee -a ~/.bashrc")
		os.system("echo 'alias rh=\"cd ~/RotorHazard/src/server\"   # goes to server file location' | tee -a ~/.bashrc")
		os.system("echo 'alias py=\"python\"  # pure laziness' | tee -a ~/.bashrc")
		os.system("echo 'alias sts=\"sudo systemctl stop rotorhazard\" # stops RH service' | tee -a ~/.bashrc")
		os.system("echo 'alias otadir=\"cd ~/RH-ota\"   # goes to server file location' | tee -a ~/.bashrc")
		os.system("echo 'alias ota=\"cd ~/RH-ota && python update.py\"  # opens updating soft' | tee -a ~/.bashrc")
		os.system("echo 'alias als=\"nano ~/.bashrc\"   #  opens this file' | tee -a ~/.bashrc")
		os.system("echo 'alias rld=\"source ~/.bashrc\"   #  reloads aliases file' | tee -a ~/.bashrc")
		os.system("echo 'alias rcfg=\"sudo raspi-config\"   #  open raspberrys configs' | tee -a ~/.bashrc")
		os.system("echo 'alias gitota=\"git clone --depth=1 https://github.com/szafranski/RH-ota.git\"   #  clones ota repo' | tee -a ~/.bashrc")
		os.system("echo 'alias otacfg=\"nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' | tee -a ~/.bashrc")
		os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && cp distr-updater-config.json updater-config.json \"  # copies ota conf. file' | tee -a ~/.bashrc")
		os.system("echo 'alias home=\"cd ~ \"  # go homedir (without ~ sign)' | tee -a ~/.bashrc")
		os.system("echo '' | tee -a ~/.bashrc")
		os.system("echo '# After adding or changing aliases manually - reboot raspberry or type \"source ~/.bashrc\".' | tee -a ~/.bashrc")
		os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases_added >/dev/null")
		os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases2_added >/dev/null")
		print("\n\n\t\t	Aliases added successfully")
		sleep(2)
		featuresMenu()
	print("""\n\n\t\t
	Aliases in Linux act like shortcuts or referances to another commands. 
	You can use them every time when you operates in the terminal window. 
	For example instead of typing 'python ~/RotorHazard/src/server/server.py' 
	you can just type 'ss' (server start) etc. Aliases can be modified and added 
	anytime you want. You just have to open '~./bashrc' file in text editor 
	- like 'nano'. After that you have reboot or type 'source ~/.bashrc'. \n
	"""+bcolors.BOLD+"""Alias			Command					  What it does	\n
	ss  	 -->  cd ~/RotorH(...)server && python server.py # starts the RH-server\t
	cfg  	 -->  nano ~/RotorHazard/src/server/config.json	 # opens config.json file\t
	rh   	 -->  cd ~/RotorHazard/src/server   		 # goes to server file location\t
	py   	 -->  python  					 # pure laziness\t
	sts   	 -->  sudo systemctl stop rotorhazard 		 # stops RH service if was started\t
	otadir   -->  cd ~/RH-ota   				 # goes to main server file location\t
	ota   	 -->  cd ~/RH-ota && python update.py  		 # opens updating soft\t
	als   	 -->  nano ~/.bashrc   				 # opens this file\t
	rld   	 -->  source ~/.bashrc   			 # reloads aliases file \t
	rcfg   	 -->  sudo raspi-config   			 # open raspberry's configs\t
	gitota 	 -->  git clone https://github.com/sza(...) 	 # clones ota repo\t
	otacfg   -->  nano ~/RH-ota/updater-config.json 	 # opens updater conf. file\t
	otacpcfg -->  cd (...)  cp distr (...) config.json 	 # copies ota cfg.\t
	home	 -->  cd ~ 	 				 # go homedir (without ~ sign)\t\t\n
	"""+bcolors.ENDC+"""
		\tDo you want to use above aliases in your system?\n\t
		\tReboot should be performed after adding those""")
	selection=str(raw_input("\n\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		if os.path.exists("/home/"+user+"/.ota_markers/.aliases_added") == True:
			print("\n\n\t\tLooks like you already have aliases added. Do you want to continue anyway?\n")
			selection=str(raw_input("\t\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
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
	def addUpdater():
		print("\nPermissions required so 'zip' and 'unzip' program can be downloaded.")
		os.system("sudo apt install zip unzip")
		os.system("""echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc""")
		os.system("""echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc""")
	clearTheScreen()
	logoTop()
	if os.path.exists("/home/"+user+"/.ota_markers/.updater_self") == True:
		print("""\n\n """+bcolors.BOLD+"""
	If you want to update this program and download new firmware, \n
	prepared for Arduino nodes - so you can next flash them \n\t\t
	- you have to type 'updateupdater' or 'uu' in the terminal window.\n\n\t\t
	Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",\n\t\t
	so you allways know what firmware version updater contains.\n\t\t
	For example "2.2.5c" contains nodes firmware with "API level 22" etc.\n\t\t
	Be sure that you have internet connection established."""+bcolors.ENDC+"""\n\n """)
		print("""\n\t"""+bcolors.GREEN+"""\t\t
		Exit program by pressing 'e' """+bcolors.ENDC+"""\n\t\t
		Force updater planting again by pressing 'f'\n"""+bcolors.YELLOW+"""\t\t\t
		Go back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
		selection=str(raw_input(""))
		if selection=='e':
			sys.exit()
		if selection=='b':
			featuresMenu()
		if selection=='f':
			addUpdater()
		else :
			selfUpdater()
	else:
		addUpdater()
		sleep(0.1)
		os.system("echo 'updater marker' | tee -a ~/.ota_markers/.updater_self >/dev/null")
		clearTheScreen()
		logoTop()
		print("""\n\n """+bcolors.BOLD+"""
	If you want to update this program and download new firmware, \n
	prepared for Arduino nodes - so you can next flash them  \n\t\t
	- you have to reboot the Raspberry. Next step is to type  \n\t\t
	'updateupdater' or 'uu' in the terminal window.\n\t\t
	Next time you won't have to reboot before updating.\n\n\t\t
	Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",\n\t\t
	so you allways know what firmware version updater contains.\n\t\t
	For example 2.2.5c contains nodes firmware with API 22 etc.\n\t\t
	Be sure that you have internet connection established."""+bcolors.ENDC+"""\n""")
		print("""\n\t\t\t"""+bcolors.GREEN+"""\t
		Reboot by pressing 'r' """+bcolors.ENDC+"""\n\t\t\t\t"""+bcolors.YELLOW+"""\t
		Go back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
		selection=str(raw_input(""))
		if selection=='r':
			os.system("sudo reboot")
		if selection=='b':
			featuresMenu()
		else :
			selfUpdater()

def featuresMenu():
	clearTheScreen()
	logoTop()
	print("\n\n\n\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"FEATURES MENU\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"1 - Install avrdude\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"2 - Enable serial protocol\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"3 - Access Point and Internet - new\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"4 - Useful aliases\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"5 - Self updater \n"+bcolors.ENDC)
	print("			"+bcolors.YELLOW+bcolors.BOLD+"e - Exit to main menu"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1':
		avrDude()
	if selection== '2':
		serialMenu()
	if selection=='3':
		os.system("python ./net_and_ap.py")
	if selection=='4':
		aliasesMenu()
	if selection=='5':
		selfUpdater()
	if selection=='e':
		mainMenu()
	else:
		featuresMenu()

def firstTime():
	def UpdateNotes():
		clearTheScreen()
		os.system("less ./update-notes.md")
		#with open('./update-notes.txt', 'rt') as f:
		#	for line in f:
		#		print line.replace('\n', '').replace('####', '')
		#selection=str(raw_input(bcolors.GREEN+"\n\t\t'k' - OK, go to Main Menu"+bcolors.ENDC))
		#if selection=='k':
		#	mainMenu()
	def secondPage():
		clearTheScreen()
		print("""\n\n
		"""+bcolors.BOLD+bcolors.UNDERLINE+"""\t\tCONFIGURATION PROCESS"""+bcolors.ENDC+"""\n\n
	"""+bcolors.BOLD+"""Configuration process can be assisted with a wizard. 
	You have to enter point 5. of Main Menu and apply right values.\n
	It will configure this software, not RotorHazard server itself. \n
	Thing like amount of used LEDs or password to admin page of RH
	should be configured separately.\n\n
	Possible RotorHazard server versions:\n
	> """+bcolors.BLUE+"""\"stable\""""+bcolors.ENDC+bcolors.BOLD+""" - last stable release (can be from before few days or few months)\n
	> """+bcolors.BLUE+"""\"beta\""""+bcolors.ENDC+bcolors.BOLD+"""   - last 'beta' release (usually has about few weeks, quite stable)\n
	> """+bcolors.BLUE+"""\"master\""""+bcolors.ENDC+bcolors.BOLD+""" - absolutely newest features implemented (even if not well tested)"""+bcolors.ENDC+"""\n""")
		print("\n\n\t'f' - first page'"+bcolors.GREEN+"\t'u' - see update notes'"+bcolors.ENDC+bcolors.YELLOW+"\t\t'b' - back to menu"+bcolors.ENDC+"\n\n")
		selection=str(raw_input(""))
		if selection=='f':
			firstPage()
		if selection=='b':
			mainMenu()
		if selection=='u':
			UpdateNotes()
		else :
			secondPage()
	def firstPage():
		clearTheScreen()
		print(bcolors.BOLD+"""\n\n
	You can use all implemened features, but if you want to be able to program\n
	Arduino-based nodes - enter Features menu and begin with first 2 points.\n\n
	Also remember about setting up config file - check second page.  \n\n
	This program has ability to perform 'self-updates'. Check "Features menu".\n\n
	More info here: https://www.instructables.com/id/RotorHazard-Updater/\n
	and in how_to folder - look for PDF file.\n\n 
	If you found any bug - please report via GitHub or Facebook.\n\n
	\t\tEnjoy!\n\t\t\t\t\t\t\t\tSzafran\n """+bcolors.ENDC)
		print("\n\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t'u' - see update notes'"+bcolors.YELLOW+"\t\t'b' - back to menu"+bcolors.ENDC+"\n\n")
		selection=str(raw_input(""))
		if selection=='s':
			secondPage()
		if selection=='u':
			UpdateNotes()
		if selection=='b':
			mainMenu()
		else :
			firstPage()
	firstPage()

def end():
		clearTheScreen()
		print("\n\n")
		image()
		print("\t\t\t\tHappy flyin'!\n")
		sleep(1.3)
		clearTheScreen()
		sys.exit()

def mainMenu():
	clearTheScreen()
	logoTop()
	print("\n\n\n\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"MAIN MENU\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"1 - Server software installation and update\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"3 - Start the server now\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"4 - Additional features\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"5 - Info + first time here - READ!\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"6 - Enter configuration wizard\n"+bcolors.ENDC)
	print("			"+bcolors.YELLOW+bcolors.BOLD+"e - Exit"+bcolors.ENDC)
	# valid_options = ['1', '2', '3', '4', '5', 'e']  ### another option for error catching
	# while True:
		# selection=raw_input().strip()
		# if selection in valid_options:
			# break
		# else:
			# print("too big fingers :( wrong command. focus and try again!")
	selection=str(raw_input(""))
	if selection=='1':
		os.system("python ./rpi_update.py")   ### opens raspberry updating file
	if selection=='2':
		os.system("python ./nodes_update.py")   ### opens nodes updating file
	if selection=='3':
		clearTheScreen()
		os.system("sh server_start.sh")
		#os.system("python ./server_start.py")
	if selection=='4':
		featuresMenu()
	if selection=='5':
		firstTime()
	if selection=='6':
		os.system("python ./conf_wizard.py")
	if selection=='e':
		end()
	if selection=='2dev':
		os.system("python ./nodes_update_dev.py")   ### opens nodes updating file
	else:
		mainMenu()
mainMenu()
