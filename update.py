####To do:####
# avrdude test - maybe

from time import sleep
import os
import platform
import sys
import json
import subprocess

updater_version = '2.2.8h'  ### version of THIS program - has nothing to do with the RH version
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
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

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
		###\t\t\t"""+bcolors.ORANGE+"""     """+bcolors.BOLD+"""RotorHazard        """+bcolors.ENDC+"""\t\t    ###
		###                                                                 ###
		###                     """+bcolors.BOLD+"""OTA Updater and Manager"""+bcolors.ENDC+"""                     ###
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
		###\t\t"""+bcolors.BOLD+"""Flashing firmware onto """+str(nodes_number)+""" nodes - DONE"""+bcolors.ENDC+"""\t\t    ###
		###                                                                 ###
		###                          """+bcolors.BOLD+"""Thank you!"""+bcolors.ENDC+"""                             ###
		###                                                                 ###
		#######################################################################
		\n\n""")

def compatibility():               ### adds compatibility and fixes with previous versions
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
			os.system("sed -i 's/RotorHazard OTA Manager updated/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias updateupdater=\"cd ~ && sudo cp ~/RH-ota/self.py ~/.ota_markers/self.py && sudo python ~/.ota_markers/self.py \"  # part of self-updater' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'starts the server'):
			os.system("sed -i 's/alias ss/# alias ss/g' "+homedir+"/.bashrc")
			os.system("sed -i 's/starts the server/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias ss=\"cd ~/RotorHazard/src/server && python server.py\"   #  starts the RH-server' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'opens updating script'):
			os.system("sed -i 's/alias ota=/# alias ota=/g' "+homedir+"/.bashrc")
			os.system("sed -i 's/opens updating script/old alias/g' "+homedir+"/.bashrc")
			os.system("echo 'alias ota=\"cd ~/RH-ota && python update.py\"  # opens updating soft' | tee -a ~/.bashrc >/dev/null")
		if check_if_string_in_file(homedir+'/.bashrc', 'part of self-updater'):
			os.system("sed -i 's/part of self-updater/part of self updater/g' "+homedir+"/.bashrc")
			os.system("echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null")
		if os.path.exists(homedir+"/.ota_markers/.aliases_added") == True:
			if os.path.exists(homedir+"/.ota_markers/.aliases2_added") == False:
				os.system("echo 'alias otacfg=\"sudo nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && sudo cp distr-updater-config.json updater-config.json \"  # copies ota conf. file' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'alias home=\"cd ~ \"  # go homedir (without ~ sign)' | tee -a ~/.bashrc >/dev/null")
				os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases2_added >/dev/null")
		if os.path.exists("./updater-config.json") == True:
			if not check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"pins_assignment"'):
				os.system("sed -i 's/\"debug_mode\" : 0/\"debug_mode\" : 0,/g' "+homedir+"/RH-ota/updater-config.json")
				os.system("sed -i 's/\"debug_mode\" : 1/\"debug_mode\" : 1,/g' "+homedir+"/RH-ota/updater-config.json")
				os.system("sed -i 's/}/	\"pins_assignment\" : \"default\" /g' "+homedir+"/RH-ota/updater-config.json")
			if check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"pins_assignment"'):
				if not check_if_string_in_file(homedir+'/RH-ota/updater-config.json', '"updates_without_pdf"'):
					os.system("sed -i 's/\"pins_assignment\" : \"default\"/\"pins_assignment\" : \"default\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/\"pins_assignment\" : \"custom\"/\"pins_assignment\" : \"custom\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/\"pins_assignment\" : \"PCB\"/\"pins_assignment\" : \"PCB\",/g' "+homedir+"/RH-ota/updater-config.json")
					os.system("sed -i 's/}/	\"updates_without_pdf\" : 0 /g' "+homedir+"/RH-ota/updater-config.json")
					os.system("echo '}' | tee -a "+homedir+"/RH-ota/updater-config.json >/dev/null 2>&1")

#		if check_if_string_in_file(homedir+'/.bashrc', 'rld'):
#			rldals.communicate()

def first ():
	if linux_testing == False:
		os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &")
	compatibility()
	clearTheScreen()
	print("\n\n")
	image()
	print("\t\t\t\t\t Updater version: "+str(updater_version))
	sleep(1.1)
first()

def avrDude():
	sleep(0.12)
	clearTheScreen()
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
	clearTheScreen()
	sleep(0.12)
	logoTop()
	sleep(0.12)
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
	sleep(0.2)
	clearTheScreen()
	sleep(0.2)
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
		os.system("echo 'alias otacfg=\"sudo nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' | tee -a ~/.bashrc")
		os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && sudo cp distr-updater-config.json updater-config.json \"  # copies ota conf. file' | tee -a ~/.bashrc")
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
	otacfg   -->  sudo nano ~/RH-ota/updater-config.json 	 # opens updater conf. file\t
	otacpcfg -->  cd (...) sudo cp distr (...) config.json 	 # copies ota cfg.\t
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
	sleep(0.12)
	clearTheScreen()
	sleep(0.12)
	logoTop()
	sleep(0.12)
	if os.path.exists("/home/"+user+"/.ota_markers/.updater_self") == True:
		print("""\n\n """+bcolors.BOLD+"""
		If you want to update this program and download new firmware, \n
		prepared for Arduino nodes - so you can next flash them \n\t\t
		- you have to type 'updateupdater' or 'uu' in the terminal window.\n\n\t\t
		Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",\n\t\t
		so you allways know what firmware version updater contains.\n\t\t
		For example "2.2.5c" contains nodes firmware with "API level 22" etc.\n\t\t
		Be sure that you have internet connection established."""+bcolors.ENDC+"""\n\n """)
		print("""\n\t\t\t\t"""+bcolors.GREEN+"""\tExit program by pressing 'e' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
		+bcolors.YELLOW+"""\tGo back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
		selection=str(raw_input(""))
		if selection=='e':
			sys.exit()
		if selection=='b':
			featuresMenu()
		else :
			selfUpdater()
	else:
		os.system("""echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc""")
		os.system("""echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc""")
		sleep(0.1)
		os.system("echo 'updater marker' | tee -a ~/.ota_markers/.updater_self >/dev/null")
		sleep(0.12)
		clearTheScreen()
		sleep(0.12)
		logoTop()
		sleep(0.12)
		print("""\n\n """+bcolors.BOLD+"""
		If you want to update this program and download new firmware, \n
		prepared for Arduino nodes - so you can next flash them  \n\t\t
		- you have to reboot the Raspberry. Next step is to type  \n\t\t
		'updateupdater' in the terminal window.\n\t\t
		Next time you won't have to reboot before updating.\n\n\t\t
		Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",\n\t\t
		so you allways know what firmware version updater contains.\n\t\t
		For example 2.2.1 contains nodes firmware with API 22 etc.\n\t\t
		Be sure that you have internet connection established."""+bcolors.ENDC+"""\n\n """)
		print("""\n\t\t\t\t"""+bcolors.GREEN+"""\tReboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
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
	clearTheScreen()
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\n\t\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"FEATURES MENU\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+bcolors.BOLD+"1 - Install avrdude\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+bcolors.BOLD+"2 - Enable serial protocol\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"3 - Access Point and Internet - new\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"4 - Useful aliases\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"5 - Self updater \n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.YELLOW+bcolors.BOLD+"e - Exit to main menu"+bcolors.ENDC)
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

def serverStart():
	sleep(0.12)
	clearTheScreen()
	sleep(0.12)
	print("\n\n\t\tPlease wait...\n\n")
	print("\n")
	os.chdir("/home/"+user+"/RotorHazard/src/server")
	os.system("python server.py")

def firstTime():
	def secondPage():
		sleep(0.12)
		clearTheScreen()
		sleep(0.12)
		print("""\n\n
		"""+bcolors.BOLD+bcolors.UNDERLINE+"""\t\t\tCONFIGURATION FILE"""+bcolors.ENDC+"""\n\n
		"""+bcolors.BOLD+"""Copy "distr-updater-config.json" from same folder to "updater-config.json". \n
		Use: 'cp distr-updater-config.json updater-config.json'.\n
		Next, edit new file using 'nano' command, make changes and save. \n\n
		Possible RotorHazard versions:\n
		> """+bcolors.BLUE+"""\"stable\""""+bcolors.ENDC+bcolors.BOLD+""" - last stable release (can be from before few months)\n
		> """+bcolors.BLUE+"""\"beta\""""+bcolors.ENDC+bcolors.BOLD+"""   - last beta release (usually few weeks, quite stable)\n
		> """+bcolors.BLUE+"""\"master\""""+bcolors.ENDC+bcolors.BOLD+""" - absolutely newest release (even if not well tested)"""+bcolors.ENDC+"""\n
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
		clearTheScreen()
		sleep(0.12)
		print(bcolors.BOLD+"""\n\n\n
		You can use all implemened features, but if you want to be able to program\n
		Arduino-based nodes - enter Features menu and begin with first 2 points.\n\n
		Also remember about setting up config file - check second page.  \n\n
		This program has ability to perform 'self-updates'. Check "Features menu".\n\n
		More info here: https://www.instructables.com/id/RotorHazard-Updater/\n
		and in how_to folder - look for PDF file.\n\n 
		\t\n\t\t\tEnjoy!\n\t\t\t\t\t\t\t\tSzafran\n\n\n """+bcolors.ENDC)
		selection=str(raw_input("\t\t\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
		if selection=='s':
			secondPage()
		if selection=='b':
			mainMenu()
		else :
			firstPage()
	firstPage()

def end():
		clearTheScreen()
		print("\n\n")
		image()
		print("\t\t\t\t\t  Happy flyin'!\n")
		sleep(1.3)
		clearTheScreen()
		sys.exit()

def mainMenu():
	sleep(0.12)
	clearTheScreen()
	sleep(0.12)
	logoTop()
	sleep(0.12)
	print("\n\n\n\t\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"MAIN MENU\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+bcolors.BOLD+"1 - Server software installation and update\n	"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BLUE+bcolors.BOLD+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"3 - Start the server now\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"4 - Additional features\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.BOLD+"5 - This is my first time - READ!\n"+bcolors.ENDC)
	print("\t\t\t   "+bcolors.YELLOW+bcolors.BOLD+"e - Exit"+bcolors.ENDC)
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
	if selection=='e':
		end()
	else: 
		mainMenu()
mainMenu()
