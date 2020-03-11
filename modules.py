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
	sleep(0.05)

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
