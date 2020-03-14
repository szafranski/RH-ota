from time import sleep
import os
import platform
import sys
import json
from modules import clearTheScreen, bcolors, logoTop

homedir = os.path.expanduser('~')

clearTheScreen()
logoTop()

def confCheck():
	global conf_now_FLAG
	if os.path.exists("./updater-config.json") == True:
		print("\n\t\tLooks that you have OTA software already configured.")
		valid_options = ['y', 'yes', 'n', 'no']
		while True:
			cont_conf = raw_input("\n\t\tOverwrite and continue anyway? [yes/no]\t\t").strip()
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
		os.system("rm .wizarded-updater-config.json >/dev/null 2>&1")
		name = raw_input("\nWhat is your user name on Raspberry Pi? [default: pi]\t\t\t")
		os.system("echo '{' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
		os.system("echo '	\"pi_user\" : \""+name+"\",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
		while True:
			version = raw_input("\nWhat RotorHazard version will you use? ["+bcolors.UNDERLINE+"stable"+bcolors.ENDC+" | beta | master]\t\t")
			version_valid_options = ['master','stable','beta']
			if not version in version_valid_options:
				print("\nPlease enter correct value!")
			else:
				os.system("echo '	\"RH_version\" : \""+version+"\",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
				break
		debug_user = raw_input("\nWhat is you user name on debugging OS? [default: racer]\t\t\t")
		os.system("echo '	\"debug_user\" : \""+debug_user+"\",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
		code = raw_input("\nWhat is your country code? [default: GB]\t\t\t\t")
		os.system("echo '	\"country\" : \""+code+"\",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
		while True:
			nodes = raw_input("\nHow many nodes will you use in your system? [min: 0/1 | max: 8]\t\t")
			if (nodes.isdigit()==False) or (int(nodes) >8):
				print("\nPlease enter correct value!")
			else:
				os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
				break
		while True:
			debug_mode = raw_input("\nWill you use \"OTA\" software in a debug mode? [yes/no | default: no]\t")
			debug_mode_allowed_values = ['yes','no','1','0','y','n']
			if not debug_mode in debug_mode_allowed_values:
				print("\nPlease enter correct value!")
			else:
				if debug_mode in ['yes','1','y']:
					debug_mode_val = '1'
				elif debug_mode in ['no','0','n']:
					debug_mode_val = '0'
				os.system("echo '	\"debug_mode\" : "+debug_mode_val+",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
				break
		while True:
			pins_assign = raw_input("\nPins assignment? [default/custom/PCB | default: default]\t\t")
			pins_valid_options = ['default','PCB','pcb','custom']
			if not pins_assign in pins_valid_options:
				print("\nPlease enter correct value!")
			else:
				os.system("echo '	\"pins_assignment\" : \""+pins_assign+"\",' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
				break
		while True:
			no_pdf = raw_input("\nUpdates without PDF? [yes/no | default: yes]\t\t\t\t")
			no_pdf_allowed_values = ['yes','no','1','0','y','n']
			if not no_pdf in no_pdf_allowed_values:
				print("\nPlease enter correct value!")
			else:
				if no_pdf in ['yes','1','y']:
					no_pdf_val = '1'
				elif no_pdf in ['no','0','n']:
					no_pdf_val = '0'
				os.system("echo '	\"updates_without_pdf\" : "+no_pdf_val+"' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")
				break
		os.system("echo '}' | tee -a "+homedir+"/RH-ota/.wizarded-updater-config.json >/dev/null 2>&1")

		print("""\n\n\t\t\t"""+bcolors.UNDERLINE+"""CONFIGURATION"""+bcolors.ENDC+""":\n\t
		User name: \t\t"""+name+"""
		RotorHazard version: \t"""+version+"""
		Debug user name: \t"""+debug_user+"""
		Country code: \t\t"""+code+"""
		Nodes amount: \t\t"""+nodes+"""
		Debug mode: \t\t"""+debug_mode+"""
		Pins assignment: \t"""+pins_assign+"""
		Updates without PDF: \t"""+no_pdf+"""\n\n""")

		print("Please check. Confirm? [yes/change/abort]\n")
		valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
		while True:
			selection=raw_input().strip()
			if selection in valid_options:
				break
			else:
				print("too big fingers :( wrong command. try again! :)")
		if selection == 'y' or selection ==  'yes':
			os.system("mv .wizarded-updater-config.json updater-config.json")
			print("Configuration saved.\n")
			sleep(0.5)
			break
		if selection in ['change','n','no']:
			continue
		if selection == 'abort':
			print("Configuration aborted.\n")
			sleep(0.5)
			break
else:
	os.system("exit")
