from time import sleep
import os
import platform
import sys
import json

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

myPlace = data['country']

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
		print("\t\t\t\t\t  Linux PC version")
	if os.path.exists("./updater-config.json") == False:
		print("\t\t\t    Looks that you haven't set up config file yet!")

# Set the WiFi country in raspi-config's Localisation Options:
# sudo raspi-config
# ( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )

def stepFour():
	with open('./net_ap/net_steps.txt', 'rt') as f:
		for line in f:
			if '### step4' in line:
				for line in f:
					print line.replace('####', '')
					if '####' in line:
						break
	print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
			+bcolors.YELLOW+"""    Exit by pressing 'e'"""+bcolors.ENDC)
	selection=str(raw_input(""))
	if selection=='r':
		os.system("sudo reboot")
	if selection=='e':
		sys.exit()
	else :
		main()

def stepThree():
	os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.ap")
	clearTheScreen()
	with open('./net_ap/net_steps.txt', 'rt') as f:
		for line in f:
			if '### step3' in line:
				for line in f:
					print line.replace('####', '')
					if '####' in line:
						break
	print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
			+bcolors.YELLOW+"""    Exit by pressing 'e'"""+bcolors.ENDC+"""\n""")
	selection=str(raw_input(""))
	if selection=='r':
		os.system("sudo reboot")
	if selection=='e':
		sys.exit()
	else :
		main()

def stepTwo():
	clearTheScreen()
	with open('./net_ap/net_steps.txt', 'rt') as f:
		for line in f:
			if '### step2' in line:
				for line in f:
					print line.replace('\n', '').replace('####', '')
					if '####' in line:
						break

def confCopy():
	os.system("echo 'alias netcfg=\"cp /etc/dhcpcd.conf.net /etc/dhcpcd.conf \"  # net conf' | sudo tee -a ~/.bashrc")
	os.system("echo 'alias apcfg=\"cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf \"  # net conf' | sudo tee -a ~/.bashrc")
	os.system("sudo cp ./net_ap/dhcpcd.conf.net /etc/dhcpcd.conf.net")
	os.system("sudo cp ./net_ap/dhcpcd.conf.ap /etc/dhcpcd.conf.ap")
	os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig")
	os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig")
	os.system("sudo cp ./net_ap/dnsmasq.conf.net /etc/dnsmasq.conf.net")

def stepOne():
	confCopy()
	os.system("sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf")
	os.system("echo 'country="+myPlace+"'| sudo  tee -a /boot/config.txt")
	os.system("sudo apt-get update && sudo apt-get upgrade -y")
	os.system("sudo apt install curl -y")
	os.system("curl -sL https://install.raspap.com | bash -s -- -y")
	stepTwo()
	print("""\n\t\t\t\t"""+bcolors.GREEN+"""Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
			+bcolors.YELLOW+"""Exit by pressing 'e'"""+bcolors.ENDC+"""\n""")
	selection=str(raw_input(""))
	if selection=='r':
		os.system("sudo reboot")
	if selection=='e':
		sys.exit()
	else :
		main()

def stepZero():
	sleep(0.05)
	clearTheScreen()
	sleep(0.05)
	logoTop()
	sleep(0.05)
	with open('./net_ap/net_steps.txt', 'rt') as f:
		for line in f:
			if '### step1' in line:
				for line in f:
					print line.replace('\n', '').replace('####', '')
					if '####' in line:
						break
	print("""\n
	\t\t"""+bcolors.GREEN+"""'y' - Yes, let's do it """+bcolors.ENDC+"""\n
	\t\t'3' - enters "Step 3." - check it after first two steps\n
	\t\t'x' - enters Access Point extra menu - info after operation\n
	\t\t"""+bcolors.YELLOW+"""'e' - exit to main menu"""+bcolors.ENDC+"""\n""")
	selection=str(raw_input(""))
	if selection=='y':
		stepOne()
	if selection=='3':
		stepThree()
	if selection=='x':
		apMenu()
	if selection=='e':
		sys.exit()
	else :
		main()

def apMenu():
	def secondPage():
		sleep(0.05)
		clearTheScreen()
		sleep(0.05)
		with open('./net_ap/net_steps.txt', 'rt') as f:
			for line in f:
				if '### step last - page 2' in line:
					for line in f:
						print line.replace('\n', '').replace('####', '')
						if '####' in line:
							break
		selection=str(raw_input("\t\t\t"+bcolors.GREEN+"'k' - OK '"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
		if selection=='k':
			sys.exit()
		if selection=='b':
			firstPage()
		else :
			secondPage()
	def firstPage():
		sleep(0.05)
		clearTheScreen()
		sleep(0.05)
		logoTop()
		sleep(0.05)
		with open('./net_ap/net_steps.txt', 'rt') as f:
			for line in f:
				if '### step last - page 1' in line:
					for line in f:
						print line.replace('\n', '').replace('####', '')
						if '####' in line:
							break
		selection=str(raw_input("\t\t\t"+bcolors.GREEN+"'s' - second page'"+bcolors.ENDC+"\t\t"+bcolors.YELLOW+"'b' - go back"+bcolors.ENDC+"\n"))
		if selection=='s':
			secondPage()
		if selection=='b':
			main()
		else :
			firstPage()
	firstPage()

def main():
	stepZero()
	stepOne()
main()
