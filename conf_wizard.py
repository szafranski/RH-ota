from time import sleep
import os
import platform
import sys
import json

homedir = os.path.expanduser('~')

while True:
	print("\nPlease enter your configuration data. May be changed later.\n") 
	os.system("rm updater-config-wizarded.json >/dev/null 2>&1")
	name = raw_input("\nWhat is your user name on Raspberry Pi? [default: pi]\t")
	os.system("echo '{' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	os.system("echo '	\"pi_user\" : \""+name+"\",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	version = raw_input("\nWhat is your preffered RotorHazard version? [stable | beta | master]\t")
	os.system("echo '	\"RH_version\" : \""+version+"\",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	debug_user = raw_input("\nWhat is you name on debug OS? [default: n/a]\t")
	os.system("echo '	\"debug_user\" : \""+debug_user+"\",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	code = raw_input("\nWhat is your country code? [default: GB]\t")
	os.system("echo '	\"country\" : \""+code+"\",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	nodes = raw_input("\nHow many nodes will you use in your system? [default: 4 | max: 8]\t")
	os.system("echo '	\"nodes_number\" : "+nodes+",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	debug_mode = raw_input("\nWill you use debug mode? [1 - yes | 0 - just a normal mode]\t")
	os.system("echo '	\"debug_mode\" : "+debug_mode+",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	pins_assign = raw_input("\nPins assignment? [default | custom | PCB; default: default]\t")
	os.system("echo '	\"pins_assignment\" : \""+pins_assign+"\",' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	no_pdf = raw_input("\nUpdates without PDF? [1 - yes | 0 - no; default: 1]\t")
	os.system("echo '	\"updates_without_pdf\" : "+no_pdf+"' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")
	os.system("echo '}' | tee -a "+homedir+"/RH-ota/updater-config-wizarded.json >/dev/null 2>&1")

	print("""\n\n\tCONFIGURATION:\n\t
	User name: """+name+"""
	RotorHazard version: """+version+"""
	Debug user name: """+debug_user+"""
	Country code: """+code+"""
	Nodes amount: """+nodes+"""
	Debug mode: """+debug_mode+"""
	Pins assignment: """+pins_assign+"""
	Updates without PDF: """+no_pdf+"""\n\n""")

	print("Please check. Confirm? [yes/no]\n")
	valid_options = ['y', 'yes', 'n', 'no']
	while True:
		selection=raw_input().strip()
		if selection in valid_options:
			break
		else:
			print("too big fingers :( wrong command. try again! :)")

	if selection == 'y' or selection ==  'yes':
		os.system("mv updater-config-wizarded.json test.json")
		print("Configuration saved.")
		break
	if selection == 'n' or selection == 'no':
		continue
