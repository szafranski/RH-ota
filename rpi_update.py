from time import sleep
import time
import os
import sys
import platform
import json
from modules import clearTheScreen, bcolors, logoTop, image, check_if_string_in_file#, internetCheck
# import importlib

if os.path.exists("./updater-config.json") == True:
	with open('updater-config.json') as config_file:
		data = json.load(config_file)
else:
	with open('distr-updater-config.json') as config_file:
		data = json.load(config_file)

if data['debug_mode'] == 1:
	linux_testing = True
else:
	linux_testing = False 

if linux_testing == True:
	user = data['debug_user']
else:
	user = data['pi_user']

preffered_RH_version = data['RH_version']   #### can be 'beta'or 'master' or 'user_defined' - default 'stable'

if preffered_RH_version == 'master':
	server_version = 'master'
if preffered_RH_version == 'beta':
	server_version = '2.1.0-beta.3'
if preffered_RH_version == 'stable':
	server_version = '2.1.0'
if preffered_RH_version =='custom':
	server_version = 'X.X.X'           ### paste custom version number here if you want to declare it manually

#global internet_FLAG

def internetCheck():
	print("\nPlease wait - checking internet connection state...\n")
	global internet_FLAG
	before_millis = int(round(time.time() * 1000))
	os.system(". /home/"+user+"/RH-ota/open_scripts.sh; net_check ")
	while True:
		now_millis = int(round(time.time() * 1000))
		time_passed = (now_millis - before_millis)
		if os.path.exists("./index.html") == True:
			internet_FLAG=1
			break
		elif (time_passed > 10100):
			internet_FLAG=0
			break
	os.system("rm /home/"+user+"/RH-ota/index.html > /dev/null 2>&1")
	os.system("rm /home/"+user+"/RH-ota/wget-log* > /dev/null 2>&1")
	os.system("rm /home/"+user+"/index.html > /dev/null 2>&1")
	os.system("rm /home/"+user+"/wget-log* > /dev/null 2>&1")

def first ():
	clearTheScreen()
	print("\n\n\n")
	image()
	sleep(0.5)
first()

def serverChecker():	
	global serv_installed_FLAG 
	if os.path.exists("/home/"+user+"/RotorHazard/src/server/server.py") == True:
		os.system("grep 'RELEASE_VERSION =' ~/RotorHazard/src/server/server.py > ~/.ota_markers/.server_version")
		os.system("sed -i 's/RELEASE_VERSION = \"//' ~/.ota_markers/.server_version")
		os.system("sed -i 's/\" # Public release version code//' ~/.ota_markers/.server_version")
		f = open("/home/"+user+"/.ota_markers/.server_version","r")
		for line in f:
			global server_version_name
			server_version_name = bcolors.GREEN+line+bcolors.ENDC
		serv_installed_FLAG = True
	else:
		server_version_name = bcolors.YELLOW+"""no installation found\n"""+bcolors.ENDC
		serv_installed_FLAG = False

def configChecker():
	global config_FLAG
	global config_soft
	if os.path.exists("/home/"+user+"/RotorHazard/src/server/config.json") == True:
		config_soft = bcolors.GREEN+"""configured"""+bcolors.ENDC
		config_FLAG = True
	else:
		config_soft = bcolors.YELLOW+bcolors.UNDERLINE+"""not configured"""+bcolors.ENDC
		config_FLAG = False

def sysConf():
	os.system("sudo systemctl enable ssh")
	os.system("sudo systemctl start ssh ")
	os.system("echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt")
	os.system("echo 'core_freq=250' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=spi=on' | sudo sudo tee -a /boot/config.txt  ")  
	os.system("echo 'i2c-bcm2708' | sudo tee -a /boot/config.txt")
	os.system("echo 'i2c-dev' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt")
	os.system("echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt")
	os.system("sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")
	os.system("sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf")

def endUpdate():
	print("\n\n")
	if config_FLAG == False and serv_installed_FLAG == True:
		print(bcolors.GREEN+"""\t\t'c' - configure the server now"""+bcolors.ENDC)
	else:
		print("""\t\t'c' - Reconfigure RotorHazard server""")
	print("""
		'r' - reboot - recommended when configured\n
		's' - start the server now\n"""+bcolors.YELLOW+"""
		'e' - exit now\n"""+bcolors.ENDC)
	def endMenu():
		selection=str(raw_input(""))
		if selection =='r':	
			os.system("sudo reboot")
		if selection =='e':	
			sys.exit()
		if selection =='c':	
			os.system(". /home/"+user+"/RH-ota/open_scripts.sh; configuraton_start")
			endUpdate()
		if selection =='s':	
			clearTheScreen()
			os.chdir("/home/"+user+"/RH-ota")
			os.system(". ./open_scripts.sh; server_start")
			#os.system("sh ./server_start.sh")
		else: 
			end()
	endMenu()	
	clearTheScreen()

def endInstallation():
	print("""\n\n"""+bcolors.GREEN+"""
		'c' - configure the server now - recommended\n
		'r' - reboot - recommended after configuring"""+bcolors.ENDC+"""\n
		's' - start the server now\n"""+bcolors.YELLOW+"""
		'e' - exit now\n"""+bcolors.ENDC)
	def endMenu():
		selection=str(raw_input(""))
		if selection =='r':	
			os.system("sudo reboot")
		if selection =='e':	
			sys.exit()
		if selection =='c':	
			os.system(". /home/"+user+"/RH-ota/open_scripts.sh; configuraton_start")
			endUpdate()
		if selection =='s':	
			clearTheScreen()
			os.chdir("/home/"+user+"/RH-ota")
			os.system(". ./open_scripts.sh; server_start")
			#os.system("sh ./server_start.sh")
		else: 
			end()
	endMenu()	
	clearTheScreen()

def installation():
	if linux_testing == False:
		os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &")
	internetCheck()
	if internet_FLAG==0:
		print("\nLooks like you don't have internet connection. Installation canceled.")
		sleep(2)
	else:
		print("\nInternet connection - OK")
		sleep(2)
		clearTheScreen()
		print("\n\t"+bcolors.BOLD+"Installation process has been started - please wait..."+bcolors.ENDC+" \n")
		os.system("sudo apt-get update && sudo apt-get upgrade -y")
		os.system("sudo apt autoremove -y")
		os.system("sudo apt install wget ntp libjpeg-dev i2c-tools python-dev libffi-dev python-smbus build-essential python-pip git scons swig zip -y")
		if linux_testing == True:            ### on Linux PC system
			os.system("sudo apt dist-upgrade -y")
		else:                                ### on Raspberry
			os.system("sudo apt install python-rpi.gpio")
			if conf_allowed == True:
				sysConf()
		os.system("sudo -H pip install cffi pillow")
		os.chdir("/home/"+user)
		if os.path.exists("/home/"+user+"/.old_RotorHazard.old") == False:
			os.system("mkdir /home/"+user+"/.old_RotorHazard.old")
		if os.path.exists("/home/"+user+"/RotorHazard") == True:
			os.system("cp -r /home/"+user+"/RotorHazard /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### in case of forced installation
			os.system("rm -r /home/"+user+"/RotorHazard >/dev/null 2>&1")   ### in case of forced installation
		os.system("rm /home/"+user+"/temp >/dev/null 2>&1")     ### in case of forced installation
		os.system("cp -r /home/"+user+"/RotorHazard-* /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### in case of forced installation
		os.system("rm -r /home/"+user+"/RotorHazard-* >/dev/null 2>&1")   ### in case of forced installation
		os.chdir("/home/"+user)
		os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+server_version+" -O temp.zip")
		os.system("unzip temp.zip >/dev/null ")
		os.system("rm temp.zip")
		os.system("mv /home/"+user+"/RotorHazard-"+server_version+" /home/"+user+"/RotorHazard")
		os.system("sudo -H pip install -r /home/"+user+"/RotorHazard/src/server/requirements.txt")
		os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard/src/server")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/jgarff/rpi_ws281x.git")
		os.chdir("/home/"+user+"/rpi_ws281x")
		os.system("sudo scons")
		os.chdir("/home/"+user+"/rpi_ws281x/python")
		os.system("sudo python setup.py install")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/chrisb2/pi_ina219.git")
		os.chdir("/home/"+user+"/pi_ina219")
		os.system("sudo python setup.py install")
		os.chdir("/home/"+user)
		os.system("sudo git clone https://github.com/rm-hull/bme280.git")
		os.chdir("/home/"+user+"/bme280")
		os.system("sudo python setup.py install")
		os.system("echo 'leave this file here' | sudo tee -a /home/"+user+"/.ota_markers/.installation-check_file.txt")
		os.system("sudo apt-get install openjdk-8-jdk-headless -y")
		os.system("sudo rm /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Unit]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'Description=RotorHazard Server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'After=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Service]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'WorkingDirectory=/home/"+user+"/RotorHazard/src/server' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'ExecStart=/usr/bin/python server.py' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo ' ' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo '[Install]' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("echo 'WantedBy=multi-user.target' | sudo tee -a /lib/systemd/system/rotorhazard.service")
		os.system("sudo chmod 644 /lib/systemd/system/rotorhazard.service")
		os.system("sudo systemctl daemon-reload")
		os.system("sudo systemctl enable rotorhazard.service")
		print("""\n\n\t
		##############################################
		##                                          ##
		##         """+bcolors.BOLD+bcolors.GREEN+"""Installation completed"""+bcolors.ENDC+"""           ##
		##                                          ##
		############################################## \n\n
	After rebooting please check by typing 'sudo raspi-config' \n
	if I2C, SPI and SSH protocols are active.\n""")
		endInstallation()

def update():
	if linux_testing == False:
		os.system("sudo systemctl stop rotorhazard >/dev/null 2>&1 &")
	internetCheck()
	if internet_FLAG==0:
		print("\nLooks like you don't have internet connection. Update canceled.")
		sleep(2)
	else:
		print("\nInternet connection - OK")
		sleep(2)
		clearTheScreen()
		if os.path.exists("/home/"+user+"/RotorHazard") == False:
			print("""\n\t """+bcolors.BOLD+"""
	Looks like you don't have RotorHazard server software installed for now. \n\t\t
	If so please install your server software first or you won't be able to use the timer."""+bcolors.ENDC+""" """)
			print("""\n\n\t\t"""+bcolors.GREEN+""" 
		'i' - Install the software - recommended """+ bcolors.ENDC+"""\n\t\t 
		'u' - Force update procedure\n\t\t """+bcolors.YELLOW+"""
		'a' - Abort both  \n\n """+bcolors.ENDC+""" """)
			selection=str(raw_input())
			if selection == 'i':
				conf_allowed = True
				installation()
			if selection == 'u':
				update()
			if selection == 'a':
				clearTheScreen()
				sys.exit()
			else:
				main()
		else :
			clearTheScreen()
			print("\n\t"+bcolors.BOLD+"Updating existing installation - please wait..."+bcolors.ENDC+" \n")
			os.system("sudo -H python -m pip install --upgrade pip ")
			os.system("sudo -H pip install pillow ")
			os.system("sudo apt-get install libjpeg-dev ntp -y")
			os.system("sudo apt-get update && sudo apt-get upgrade -y")
			if linux_testing == False:
				os.system("sudo apt dist-upgrade -y")
			os.system("sudo apt autoremove -y")
			if os.path.exists("/home/"+user+"/.old_RotorHazard.old") == False:
				os.system("sudo mkdir /home/"+user+"/.old_RotorHazard.old")
			os.system("sudo cp -r /home/"+user+"/RotorHazard-* /home/"+user+"/.old_RotorHazard.old/ >/dev/null 2>&1")   ### just in case of weird sys config
			os.system("sudo rm -r /home/"+user+"/RotorHazard-master >/dev/null 2>&1")   ### just in case of weird sys config
			os.system("sudo rm -r /home/"+user+"/temp.zip >/dev/null 2>&1")   ### just in case of weird sys config
			if os.path.exists("/home/"+user+"/RotorHazard.old") == True:
				os.system("sudo cp -r /home/"+user+"/RotorHazard.old /home/"+user+"/.old_RotorHazard.old/")
				os.system("sudo rm -r /home/"+user+"/RotorHazard.old")
			os.system("sudo mv /home/"+user+"/RotorHazard /home/"+user+"/RotorHazard.old")
			os.chdir("/home/"+user)
			os.system("wget https://codeload.github.com/RotorHazard/RotorHazard/zip/"+server_version+" -O temp.zip")
			os.system("unzip temp.zip >/dev/null ")
			os.system("mv /home/"+user+"/RotorHazard-"+server_version+" /home/"+user+"/RotorHazard")
			os.system("sudo rm temp.zip")
			if os.path.exists("/home/"+user+"/backup_RH_data") == False:
				os.system("sudo mkdir /home/"+user+"/backup_RH_data")
			os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard/src/server")
			os.system("sudo chmod 777 -R /home/"+user+"/RotorHazard.old")
			os.system("sudo chmod 777 -R /home/"+user+"/.old_RotorHazard.old")
			os.system("sudo chmod 777 -R /home/"+user+"/backup_RH_data")
			os.system("sudo chmod 777 -R /home/"+user+"/.ota_markers")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/config.json /home/"+user+"/RotorHazard/src/server/ >/dev/null 2>&1 &")
			os.system("cp -r /home/"+user+"/RotorHazard.old/src/server/static/image /home/"+user+"/backup_RH_data")
			os.system("cp -r /home/"+user+"/RotorHazard.old/src/server/static/image /home/"+user+"/RotorHazard/src/server/static")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/config.json /home/"+user+"/backup_RH_data >/dev/null 2>&1 &")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/database.db /home/"+user+"/RotorHazard/src/server/ >/dev/null 2>&1 &")
			os.system("cp /home/"+user+"/RotorHazard.old/src/server/database.db /home/"+user+"/backup_RH_data >/dev/null 2>&1 &")
			os.chdir("/home/"+user+"/RotorHazard/src/server")
			os.system("sudo -H pip install --upgrade --no-cache-dir -r requirements.txt")
			print("""\n\n\t
		##############################################
		##                                          ##
		##            """+bcolors.BOLD+bcolors.GREEN+"""Update completed"""+bcolors.ENDC+"""              ##
		##                                          ##
		##############################################""")
			endUpdate()

def main():
	global config_FLAG
	global serv_installed_FLAG 
	global conf_allowed
	global config_soft
	global server_version_name
	clearTheScreen()
	serverChecker()
	configChecker()
	sleep(0.1)
	print("""\n\n\t"""+bcolors.RED+bcolors.BOLD+"""AUTOMATIC UPDATE AND INSTALLATION OF ROTORHAZARD RACING TIMER SOFTWARE\n\n\t"""+bcolors.ENDC
	+bcolors.BOLD+"""You can automatically install and update RotorHazard timing software. 
	Additional depedancies and libraries also will be installed or updated.
	Current database, configs and custom bitmaps will stay on their place.
	Source of the software is set to '"""+bcolors.BLUE+server_version+bcolors.ENDC+bcolors.BOLD+"""' version from the RH repository. 
	Perform self-updating of this software, before updating server software.
	Also make sure that you are logged as user '"""+bcolors.BLUE+user+bcolors.ENDC+bcolors.BOLD+"""'. \n
	You can change those in configuration wizard in Main Menu.\n
	Server installed right now: """+server_version_name+bcolors.BOLD+"""
	RotorHazard configuration state: """+config_soft+"""\n\n\n""")
	if config_FLAG == False and serv_installed_FLAG == True:
		print(bcolors.GREEN+"""\t\t'c' - Configure RotorHazard server\n"""+bcolors.ENDC)
	else:
		print("""\t\t'c' - Reconfigure RotorHazard server\n""")
	if serv_installed_FLAG == False:
		print(bcolors.GREEN+"""\t\t'i' - Install software from skratch"""+bcolors.ENDC)
	else:
		print("""\t\t'i' - Install software from skratch""")
	print("""
		'u' - Update existing installation\n"""+bcolors.YELLOW+""" 
		'e' - Exit to Main Menu \n"""+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection =='c':
		if serv_installed_FLAG == True:
			os.system(". ./open_scripts.sh; configuraton_start")
			#os.system("python ./conf_wizard_rh.py")
		else:
			print("\n\t\tPlease install server software first")
			sleep (1.5)
	if selection =='i':	
		if (os.path.exists("/home/"+user+"/.ota_markers/.installation-check_file.txt") == True):
			clearTheScreen()
			print("""\n"""+bcolors.BOLD+"""
	Looks like you already have RotorHazard server installed
	(or at least that your system was once configured)."""+bcolors.ENDC+"""\n
	If that's the case please use """+bcolors.UNDERLINE+"""update mode"""+bcolors.ENDC+""" - 'u'
	or force installation """+bcolors.UNDERLINE+"""without"""+bcolors.ENDC+""" sys. config. - 'i'.""")
			print("""\n\n\t"""+bcolors.GREEN+""" 
		'u' - Select update mode - recommended """+ bcolors.ENDC+"""\n 
		'i' - Force installation without sys. config.\n
		'c' - Force installation and sys. config.\n """+bcolors.YELLOW+"""
		'a' - Abort both  \n """+bcolors.ENDC+""" """)
			selection=str(raw_input())
			if selection == 'u':
				update()
			if selection == 'i':
				conf_allowed = False
				installation()
			if selection == 'c':
				confirm_valid_options = ['y', 'yes','n','no','abort','a']
				while True:
					confirm = raw_input("\n\t\tAre you sure? [yes/abort]\t").strip()
					if confirm in confirm_valid_options:
						break
					else:
						print("\ntoo big fingers :( wrong command. try again! :)")
				if confirm == 'y' or confirm ==  'yes':
					conf_allowed = True
					installation()
				if confirm in ['n','no','abort','a']:
					pass
			if selection == 'a':
				clearTheScreen()
				image()
				sleep(0.5)
				sys.exit()
			else:
				main()
		else:
			conf_allowed = True
			installation()
	if selection =='u':	
		update()
	if selection =='e':	
		clearTheScreen()
		os.chdir("/home/"+user+"/RH-ota")
		image()
		sleep(0.5)
		sys.exit()
	else:
		main()
main()
