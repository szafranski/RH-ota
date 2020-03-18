from time import sleep
import os
import platform
import sys
import json
import time

#from rpi_update import internetCheck

# import subprocess

# def print_centered(s):
	# terminal_width = int(subprocess.check_output(['stty', 'size']).split()[1])
	# print s.center(terminal_width)

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

def clear_the_screen():
	sleep(0.05)
	if platform.system() == "Windows":
		os.system("cls")
	if platform.system() == "Linux":
		os.system("clear")
	else:
		print("\n" * 200)
	sleep(0.05)

def dots2sec():
	for i in range (30):
		sys.stdout.write(".")
		sys.stdout.flush()
		sleep(0.0666)
	sys.stdout.write("\n")

def percent_count():
	def backspace(n):
		sys.stdout.write((b'\x08' * n).decode()) # use \x08 char to go back   

	for i in range(101):                        # for 0 to 100
		s = str(i) + '%'                        # string for output
		sys.stdout.write(s)                     # just print
		sys.stdout.flush()                      # needed for flush when using \x08
		backspace(len(s))                       # back n chars    
		time.sleep(0.05)        

def image_show():
	with open('./resources/image.txt', 'r') as logo:
		f = logo.read()
		print(f)

def ota_image():
	with open('./resources/ota_image.txt', 'r') as file:
		f = file.read()
		print(f)

def check_if_string_in_file(file_name, string_to_search):
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

def logo_top():
	logo = '''
	\n	
	#######################################################################
	###                                                                 ###
	###               {orange}{bold} RotorHazard {endc}                 ###
	###                                                                 ###
	###                {bold}OTA Updater and Manager{endc}              ###
	###                                                                 ###
	#######################################################################
	{endc}
	'''.format(bold=bcolors.BOLD_S, underline=bcolors.UNDERLINE_S
               , endc=bcolors.ENDC_S, blue=bcolors.BLUE_S
               , yellow=bcolors.YELLOW_S
               , red=bcolors.RED_S
			   , orange=bcolors.ORANGE_S)

	print(logo)
	if linux_testing:
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
	'''
	the following are designed to be used in formatted strings
	they each have enough spaces appended so that {value}
	will be replaced with an equal number of spaces.
	'''
	HEADER_S = '\033[95m' + (' '* 9)
	ORANGE_S = '\033[33m'+ (' '* 8)
	BLUE_S = '\033[94m'+ (' '* 6)
	GREEN_S = '\033[92m'+ (' '* 7)
	YELLOW_S = '\033[93m'+ (' '* 8)
	RED_S = '\033[91m'+ (' '* 5)
	ENDC_S = '\033[0m'+ (' '* 6)
	BOLD_S = '\033[1m'+ (' '* 6)
	UNDERLINE_S = '\033[4m'+ (' '* 11)

def internet_check():
	print("\nPlease wait - checking internet connection state...\n")
	global internet_FLAG
	before_millis = int(round(time.time() * 1000))
	os.system(". /home/"+user+"/RH-ota/open_scripts.sh; net_check")
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
