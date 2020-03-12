from time import sleep
import os
import platform
import sys
import json
import time

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

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

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

def no_internetCheck():
	print("\nPlease wait - checking internet connection state...\n")
	global internet_FLAG
	before_millis = int(round(time.time() * 1000))
	os.system("timeout 3s sh "+myhomedir+"/RH-ota/net_check.sh > /dev/null 2>&1")
	while True:
		now_millis = int(round(time.time() * 1000))
		time_passed = (now_millis - before_millis)
		if os.path.exists("./index.html") == True:
			internet_FLAG=1
			break
		elif (time_passed > 3100):
			internet_FLAG=0
			break
	os.system("rm "+myhomedir+"/RH-ota/index.html > /dev/null 2>&1")
	os.system("rm "+myhomedir+"/RH-ota/wget-log* > /dev/null 2>&1")
	os.system("rm "+myhomedir+"/index.html > /dev/null 2>&1")
	os.system("rm "+myhomedir+"/wget-log* > /dev/null 2>&1")

