from time import sleep
import os
import platform
import sys
import json
from modules import clearTheScreen, bcolors, logoTop

homedir = os.path.expanduser('~')

clearTheScreen()
logoTop()

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

def confCheck():
	global conf_now_FLAG
	if os.path.exists("/home/"+user+"/RotorHazard/src/server/updater-config.json") == True:
		print("\t\tLooks that you already have RotorHazard configured.")
		valid_options = ['y', 'yes', 'n', 'no']
		while True:
			cont_conf = raw_input("\n\t\tOverwrite and continue anyway? [yes/no] ").strip()
			if cont_conf in valid_options:
				break
			else:
				print("too big fingers :( wrong command. try again! :)")
		if cont_conf == 'y' or cont_conf ==  'yes':
			conf_now_FLAG =1
			pass
		if cont_conf == 'n' or cont_conf == 'no':
			conf_now_FLAG =0
	else:
		conf_now_FLAG =1
confCheck()

if conf_now_FLAG ==1:
	while True:
		print("""\n
Please type your configuration data. It can be modified later.
Default values are not automatically applied. Type them if needed.\n""") 
		os.system("rm .wizarded-rh-config.json >/dev/null 2>&1")
		os system("cp /home/"+user+"/RotorHazard/src/server/config-dist.json /home/"+user+"/RH-ota/.wizarded-rh-config.json")
		admin_name = raw_input("\nWhat is your desired admin user name on RotorHazard page? [default: admin]\t\t\t")
		os.system("echo '{' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
		admin_pass = raw_input("\nWhat is your desired admin password on RotorHazard page? [default: rotorhazard]\t\t\t")
		while True:
			led_count = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_count.isdigit()==False) or (int(led_count) <0):
				print("\nPlease enter correct value!")
			else:
				break
		while True:
			led_pin = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_pin.isdigit()==False) or (int(led_pin) <0):
				print("\nPlease enter correct value!")
			else:
				break
		while True:
			led_inv = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_inv.isdigit()==False) or (int(led_inv) <0):
				print("\nPlease enter correct value!")
			else:
				break
		while True:
			led_channel = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_inv.isdigit()==False) or (int(led_inv) <0):
				print("\nPlease enter correct value!")
			else:
				break
		while True:
			panel_rot = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_inv.isdigit()==False) or (int(led_inv) <0):
				print("\nPlease enter correct value!")
			else:
				break
		while True:
			inv_rows = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t")
			os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
			if (led_inv.isdigit()==False) or (int(led_inv) <0):
				print("\nPlease enter correct value!")
			else:
				break
		print("""\n\n\t\t\t"""+bcolors.UNDERLINE+"""CONFIGURATION"""+bcolors.ENDC+""":\n\t
		User name: \t\t"""+name+"""
		RotorHazard version: \t"""+version+"""
		Debug user name: \t"""+debug_user+"""
		Country code: \t\t"""+code+"""
		Nodes amount: \t\t"""+nodes+"""
		Debug mode: \t\t"""+debug_mode+"""
		Pins assignment: \t"""+pins_assign+"""
		Updates without PDF: \t"""+no_pdf+"""\n\n""")

		print("Please check. Confirm? [yes/no/abort]\n")
		valid_options = ['y', 'yes', 'n', 'no', 'abort']
		while True:
			selection=raw_input().strip()
			if selection in valid_options:
				break
			else:
				print("too big fingers :( wrong command. try again! :)")

		if selection == 'y' or selection ==  'yes':
			os.system("mv .wizarded-updater-config.json updater-config.json")
			print("Configuration saved.")
			sleep(0.5)
			break
		if selection == 'n' or selection == 'no':
			continue
		if selection == 'abort':
			print("Configuration aborted.")
			sleep(0.5)
			break
else:
	os.system("exit")

