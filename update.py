from time import sleep
import os
import platform
import sys
import json
from modules import clearTheScreen, bcolors, logoTop, image, check_if_string_in_file, ota_image
from ConfigParser import ConfigParser
parser = ConfigParser()

updater_version = '2.2.9k'  ### version of THIS program - has nothing to do with the RH version
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

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

def configCheck():
	if os.path.exists("./updater-config.json") == False:
		print("""\n\t\tLooks that you haven't set up config file yet.
		Please read about configuration process - point 5
		and next enter configuration wizard - point 6.""")

def compatibility():               ### adds compatibility and fixes with previous versions
	os.system("python ./prev_comp.py")

#		if check_if_string_in_file(homedir+'/.bashrc', 'rld'):
#			rldals.communicate()

parser.read('/home/'+user+'/.ota_markers/ota_config.txt')

def updatedCheck():
	if os.path.exists("/home/"+user+"/.ota_markers/.was_updated"):
		clearTheScreen()
		logoTop()
		print("""\n\n"""+bcolors.BOLD+"""
		Software was updated recently to the new version.\n
		You can read update notes now or check them later.
		\n\n\n"""+bcolors.ENDC+bcolors.GREEN+"""
		'r' - read update notes"""+bcolors.ENDC+"""\n
		's' - skip and don't show again
		\n""")
		selection = str(raw_input())
		if selection == 'r':
			os.system("less ./docs/update-notes.txt")
		if selection == 's':
			pass
		else:
			updatedCheck()
		os.system("rm /home/"+user+"/.ota_markers/.was_updated >/dev/null 2>&1")

def first ():
	compatibility()
	clearTheScreen()
	print("\n\n")
	image()
	print("\t\t\t\t "+bcolors.BOLD+"Updater version: "+str(updater_version)+bcolors.ENDC)
	sleep(1)
	updatedCheck()

def avrDude():
	clearTheScreen()
	logoTop()
	print("\n\n\n\t\t\t\t"+bcolors.RED+"AVRDUDE MENU"+bcolors.ENDC+"\n")
	print ("\t\t\t "+bcolors.BLUE+"1 - Install avrdude"+bcolors.ENDC)
	print ("\t\t\t "+bcolors.YELLOW+"2 - Go back"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1' : 
		os.system("sudo apt-get update")
		os.system("sudo apt-get install avrdude -y")
		print ("\nDone\n")
	if selection=='2' : 
		mainMenu()
	else:
		avrDude()

def serialMenu():
	clearTheScreen()
	logoTop()
	def serialContent():
		os.system("echo 'enable_uart=1'| sudo tee -a /boot/config.txt")
		os.system("sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt")
		#os.system("echo 'functionality added' | tee -a ~/.ota_markers/.serialok")
		parser.set('added_functions','serial_added','1')
		print("""\n\n\t\tSerial port enabled successfully\n\t\t\t\t
		You have to reboot Raspberry now. Ok?\n\t\t\t\t\t
		'r' - Reboot now\t"""
		+bcolors.YELLOW+"""'b' - Go back\n\n"""+bcolors.ENDC)
		selection=str(raw_input(""))
		if selection=='r':
			os.system("sudo reboot")
		if selection== 'b':
			featuresMenu()
	print("""\n\n\t\t
		Serial port has to be enabled. 
		Without it Arduinos cannot be programmed.\n\t\t
		Do you want to enable it now?""")
	selection=str(raw_input("\n\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		#if os.path.exists("/home/"+user+"/.ota_markers/.serialok") == True:
		if parser.getint('added_functions','serial_added') == 1:
			print("\n\n\t\tLooks like you already enabled Serial port. \n\t\tDo you want to continue anyway?\n")
			selection=str(raw_input("\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
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
		os.system("echo 'alias gitota=\"git clone https://github.com/szafranski/RH-ota.git\"   #  clones ota repo' | tee -a ~/.bashrc")
		os.system("echo 'alias gitotassh=\"git clone git@github.com:szafranski/RH-ota.git && cd ~/RH-ota\"   #  clones ota repo - ssh")
		os.system("echo 'alias otacfg=\"nano ~/RH-ota/updater-config.json \"  # opens updater conf. file' | tee -a ~/.bashrc")
		os.system("echo 'alias otacpcfg=\"cd ~/RH-ota && cp distr-updater-config.json updater-config.json \"  # copies ota conf. file' | tee -a ~/.bashrc")
		os.system("echo 'alias home=\"cd ~ \"  # go homedir (without ~ sign)' | tee -a ~/.bashrc")
		os.system("echo '' | tee -a ~/.bashrc")
		os.system("echo '# After adding or changing aliases manually - reboot raspberry or type \"source ~/.bashrc\".' | tee -a ~/.bashrc")
		#os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases_added >/dev/null")
		parser.set('added_functions','aliases_1','1')
		#os.system("echo 'functionality added - leave file here' | tee -a ~/.ota_markers/.aliases2_added >/dev/null")
		parser.set('added_functions','aliases_2','1')
		print("\n\n\t\t	Aliases added successfully")
		#os.system(". ~/.bashrc && alias*")
		#os.system("cd /home/"+user+"/RH-ota && . ./open_scripts.sh; aliases_reload")
		sleep(3)
		featuresMenu()
	print("""\n\n\t\t
	Aliases in Linux act like shortcuts or referances to another commands. 
	You can use them every time when you operates in the terminal window. 
	For example instead of typing 'python ~/RotorHazard/src/server/server.py' 
	you can just type 'ss' (server start) etc. Aliases can be modified and added 
	anytime you want. You just have to open '~./bashrc' file in text editor 
	- like 'nano'. After that you have reboot or type 'source ~/.bashrc'. \n
	"""+bcolors.BOLD+"""
		Alias			What it does	\n
		ss  	 -->	starts the RotorHazard server
		cfg  	 -->	opens RH config.json file
		rh   	 -->	goes to server file directory
		py   	 -->	insted of 'python' - pure laziness
		sts   	 -->	stops RH service if was started
		otadir   -->	goes to RH server file directory
		ota   	 -->	opens this software
		als   	 -->	opens the file that containes aliases
		rld   	 -->	reloads aliases file 
		rcfg   	 -->	opens raspberry's configuration 
		gitota 	 -->	clones OTA repository
		otacfg   -->	opens updater conf. file
		otacpcfg -->	copies ota conf. file.
		home	 -->	go to the home directory (without '~' sign)\n
	"""+bcolors.ENDC+"""
		Do you want to use above aliases in your system?\n
		Reboot should be performed after adding those""")
	selection=str(raw_input("\n\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
	if selection == 'y':
		#if os.path.exists("/home/"+user+"/.ota_markers/.aliases_added") == True:
		if parser.getint('added_functions','aliases_1') == 1:
			print("\n\n\t\tLooks like you already have aliases added. \n\t\tDo you want to continue anyway?\n")
			selection=str(raw_input("\t\t\t"+bcolors.YELLOW+"Press 'y' for yes or 'a' for abort"+bcolors.ENDC+"\n"))
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
		clearTheScreen()
		logoTop()
		print("""\n
	Permissions required so 'zip' and 'unzip' program can be downloaded.
	Performed only during first instance of entering this sub-menu\n""")
		sleep(2)
		os.system("sudo echo")
		os.system("sudo apt install zip unzip")
		os.system("""echo 'alias updateupdater=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null""")
		os.system("""echo 'alias uu=\"cd ~ && cp ~/RH-ota/self.py ~/.ota_markers/self.py && python ~/.ota_markers/self.py \"  # part of self updater' | tee -a ~/.bashrc >/dev/null""")
		os.system("echo 'updater marker' | tee -a ~/.ota_markers/.updater_self >/dev/null")
	#if not os.path.exists("/home/"+user+"/.ota_markers/.updater_self") == True:
	if parser.getint('added_functions','updater_planted') == 0:
		addUpdater()
	clearTheScreen()
	logoTop()
	print(bcolors.BOLD+"""
	If you want to update this program and download new firmware, 
	prepared for Arduino nodes - so you can next flash them 
	- you can just hit 'u' now. You can also type 'updateupdater'
	or 'uu' in the terminal window.\n
	Version of the updater is related to """+bcolors.BLUE+"""nodes firmware API number"""+bcolors.ENDC+bcolors.BOLD+""",
	so you allways know what firmware version updater contains.
	For example "2.2.5c" contains nodes firmware with "API level 22".
	Self-updater will test your internet connection during every update."""+bcolors.ENDC+"""\n""")
	print(bcolors.GREEN+"""
		Update now by pressing 'u'"""+bcolors.ENDC+"""\n""")
	print(bcolors.YELLOW+"""\t\tGo back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
	selection=str(raw_input(""))
	if selection=='b':
		featuresMenu()
	if selection=='u':
		os.system(". ./open_scripts.sh; updater_from_ota")
	else :
		selfUpdater()

def featuresMenu():
	clearTheScreen()
	logoTop()
	print("\n\n\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"FEATURES MENU"+bcolors.ENDC+"\n")
	print("			"+bcolors.BLUE+bcolors.BOLD+"1 - Install AVRDUDE\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"2 - Enable serial protocol\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"3 - Access Point and Internet\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"4 - Show actuall Pi's GPIO\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"5 - Useful aliases\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"6 - Update OTA software\n"+bcolors.ENDC)
	print("			"+bcolors.YELLOW+bcolors.BOLD+"e - Exit to main menu"+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='1':
		avrDude()
	if selection== '2':
		serialMenu()
	if selection=='3':
		os.system("python ./net_and_ap.py")
	if selection=='4':
		#if not os.path.exists("/home/"+user+"/.ota_markers/.pinout_added"):
		if parser.getint('added_functions','pinout_installed') == 0:
			print("Some additional software has to be added so action can be performed. Ok?\n[yes/no]\n")
			while True:
				selection = str(raw_input())
				if selection == 'y' or selection == 'yes':
					os.system("sudo apt install python3-gpiozero") ## && echo 'pinout added' | tee -a ~/.ota_markers/.pinout_added >/dev/null")
					parser.set('added_functions','pinout_installed','1')
					break
				if selection == 'n' or selection == 'no':
					break
				else:
					continue
		#if os.path.exists("/home/"+user+"/.ota_markers/.pinout_added"):
		if parser.getint('added_functions','pinout_installed') == 1:
			os.system("pinout")
			selection = str(raw_input("\nDone? Hit 'Enter'\n"))
		else:
			print("Additional software needed. Please re-enter this menu.")
			sleep(3)
	if selection=='5':
		aliasesMenu()
	if selection=='6':
		selfUpdater()
	if selection=='e':
		mainMenu()
	else:
		featuresMenu()

def firstTime():
	def UpdateNotes():
		clearTheScreen()
		os.system("less ./docs/update-notes.txt")
	def secondPage():
		clearTheScreen()
		print("""\n\n
		"""+bcolors.BOLD+bcolors.UNDERLINE+"""\t\tCONFIGURATION PROCESS"""+bcolors.ENDC+"""\n\n
	"""+bcolors.BOLD+"""Software configuration process can be assisted with a wizard. 
	You have to enter point 5. of Main Menu and apply right values.\n
	It will configure this software, not RotorHazard server itself. \n
	Thing like amount of used LEDs or password to admin page of RotorHazard
	should be configured separately - check RotorHazard Manager in Main Menu.\n\n
	Possible RotorHazard server versions:\n
	> """+bcolors.BLUE+"""\"stable\""""+bcolors.ENDC+bcolors.BOLD+""" - last stable release (can be from before few days or few months)\n
	> """+bcolors.BLUE+"""\"beta\""""+bcolors.ENDC+bcolors.BOLD+"""   - last 'beta' release (usually has about few weeks, quite stable)\n
	> """+bcolors.BLUE+"""\"master\""""+bcolors.ENDC+bcolors.BOLD+""" - absolutely newest features implemented (even if not well tested)"""+bcolors.ENDC+"""\n""")
		print("\n\n\t'f' - first page'"+bcolors.GREEN+"\t'u' - update notes'"+bcolors.ENDC+bcolors.YELLOW+"\t'b' - back to menu"+bcolors.ENDC+"\n\n")
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
	You can use all implemened features, but if you want to be able to program
	Arduino-based nodes - enter Features menu and begin with first 2 points.\n
	Also remember about setting up config file - check second page.  \n
	This program has ability to perform 'self-updates'. Check "Features menu".\n
	More info about whole poject that this software is a part of: 
	https://www.instructables.com/id/RotorHazard-Updater/
	and in how_to folder - look for PDF file.\n
	New features and changes - see update notes section.
	If you found any bug - please report via GitHub or Facebook.\n
			Enjoy!\n\t\t\t\t\t\t\t\tSzafran\n """+bcolors.ENDC)
		print("\n\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t'u' - update notes'"+bcolors.YELLOW+"\t'b' - back to menu"+bcolors.ENDC+"\n\n")
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
		ota_image()
		print("\t\t\t\t   "+bcolors.BOLD+"Happy flyin'!"+bcolors.ENDC+"\n")
		sleep(1.3)
		clearTheScreen()
		sys.exit()

def mainMenu():
	clearTheScreen()
	logoTop()
	configCheck()
	print("\n\n\t\t\t\t"+bcolors.RED+bcolors.BOLD+bcolors.UNDERLINE+"MAIN MENU"+bcolors.ENDC+"\n")
	print("			"+bcolors.BLUE+bcolors.BOLD+"1 - RotorHazard Manager\n"+bcolors.ENDC)
	print("			"+bcolors.BLUE+bcolors.BOLD+"2 - Nodes flash and update\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"3 - Start the server now\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"4 - Additional features\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"5 - Info + first time here\n"+bcolors.ENDC)
	print("			"+bcolors.BOLD+"6 - Configuration wizard\n"+bcolors.ENDC)
	print("			"+bcolors.YELLOW+bcolors.BOLD+"e - Exit"+bcolors.ENDC)
	selection=str(raw_input())
	if selection=='1':
		os.system("python ./rpi_update.py")   ### opens raspberry updating file
	if selection=='2':
		os.system("python ./nodes_update.py")   ### opens nodes updating file
	if selection=='3':
		clearTheScreen()
		os.system(". ./open_scripts.sh; server_start")
	if selection=='4':
		featuresMenu()
	if selection=='5':
		firstTime()
	if selection=='6':
		os.system("python ./conf_wizard_ota.py")
	if selection=='e':
		end()
	if selection=='2dev':
		os.system("python ./.dev/done_nodes_update_dev.py")   ### opens nodes updating file
	else:
		mainMenu()
	with open(''+homedir+'/.ota_markers/ota_config.txt', 'wb') as configfile:
		parser.write(configfile)

#if __name__ == "__main__":
first()
mainMenu()
