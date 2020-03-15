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
	if os.path.exists("/home/"+user+"/RotorHazard/src/server/config.json") == True:
		print("\n\t\tLooks that you already have RotorHazard server configured.")
		valid_options = ['y', 'yes', 'n', 'no']
		while True:
			cont_conf = raw_input("\n\t\tOverwrite and continue anyway? [yes/no]\t\t").strip()
			if cont_conf in valid_options:
				break
			else:
				print("\ntoo big fingers :( wrong command. try again! :)")
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
		os.system("rm /home/"+user+"/.wizarded-rh-config.json >/dev/null 2>&1")
		os.system("cp /home/"+user+"/RotorHazard/src/server/config-dist.json /home/"+user+"/RH-ota/.wizarded-rh-config.json")
		admin_name = raw_input("\nWhat will be admin user name on RotorHazard page? [default: admin]\t")
		os.system("sed -i 's/\"ADMIN_USERNAME\": \"admin\"/\"ADMIN_USERNAME\": \""+admin_name+"\"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
		admin_pass = raw_input("\nWhat will be admin password on RotorHazard page? [default: rotorhazard]\t")
		os.system("sed -i 's/\"ADMIN_PASSWORD\": \"rotorhazard\"/\"ADMIN_PASSWORD\": \""+admin_pass+"\"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
		while True:
			port = raw_input("\nWhich port will you use with RotorHazard? [default: 5000]\t\t")
			if (port.isdigit()==False) or (int(port) <0):
				print("\nPlease enter correct value!")
			else:
				os.system("sed -i 's/\"HTTP_PORT\": 5000/\"HTTP_PORT\": "+port+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
				break
		print("\nAre you planning to use LEDs in your system? [yes/no]\n")
		valid_options = ['y', 'yes', 'n', 'no']
		while True:
			selection=raw_input("\t").strip()
			if selection in valid_options:
				break
			else:
				print("\ntoo big fingers :( wrong command. try again! :)")
		if selection == 'y' or selection ==  'yes':
			led_present_FLAG=True
		if selection == 'n' or selection == 'no':
			led_present_FLAG=False
		if led_present_FLAG==True:
			while True:
				led_count = raw_input("\nHow many LEDs will you use in your system? [default: 0]\t\t\t")
				if (led_count.isdigit()==False) or (int(led_count) <0):
					print("\nPlease enter correct value!")
				else:
					os.system("sed -i 's/\"LED_COUNT\": 0/\"LED_COUNT\": "+led_count+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				led_pin = raw_input("\nWhich GPIO pin is connected to your LEDs data pin? [default: 10]\t")
				if (led_pin.isdigit()==False) or (int(led_pin) <0) or (int(led_pin) > 40):
					print("\nPlease enter correct value!")
				else:
					os.system("sed -i 's/\"LED_PIN\": 10/\"LED_PIN\": "+led_pin+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				led_inv = raw_input("\nIs LED data pin output inverted? [yes/no | default: no]\t\t\t")
				led_inv_allowed_values = ['yes','no','false','true','y','n']
				if not led_inv in led_inv_allowed_values:
					print("\nPlease enter correct value!")
				else:
					if led_inv in ['yes','1','y']:
						led_inv_val = 'true'
					elif led_inv in ['no','0','n']:
						led_inv_val = 'true'
					os.system("sed -i 's/\"LED_INVERT\": false/\"LED_INVERT\": "+led_inv_val+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				led_channel = raw_input("\nWhat channel (not pin!) will be used with your LEDs? [default: 0]\t")
				if (led_channel.isdigit()==False) or (int(led_channel) <0) or (int(led_channel) >1):
					print("\nPlease enter correct value!")
				else:
					os.system("sed -i 's/\"LED_CHANNEL\": 0/\"LED_CHANNEL\": "+led_channel+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				panel_rot = raw_input("\nBy how many degrees is your panel rotated? [0/90/180/270 | default: 0]\t")
				panel_rot_values_allowed = ['0','90','180','270']
				if not panel_rot in panel_rot_values_allowed:
					print("\nPlease enter correct value!")
				else:
					panel_val = (int(panel_rot)/90)
					os.system("sed -i 's/\"PANEL_ROTATE\": 0/\"PANEL_ROTATE\": "+str(panel_val)+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				inv_rows = raw_input("\nAre your panel rows inverted? [yes/no | default: no]\t\t\t")
				inv_rows_allowed_values = ['yes','no','false','true','y','n']
				if not inv_rows in inv_rows_allowed_values:
					print("\nPlease enter correct value!")
				else:
					if inv_rows in ['yes','1','y']:
						inv_rows_val = 'true'
					elif inv_rows in ['no','0','n']:
						inv_rows_val = 'true'
					os.system("sed -i 's/\"INVERTED_PANEL_ROWS\": \"false\"/\"INVERTED_PANEL_ROWS\": \""+inv_rows_val+"\"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break

		if led_present_FLAG==False:
			led_count = '0'
			led_pin = '10'
			led_inv = 'false'
			led_channel = '0'
			panel_rot = '0'
			inv_rows = 'false'
			print("\nLED configuration set to default values.\n\n")
			sleep(1.2)
			
		print("\nDo you want to enter advanced wizard? [yes/no]\n")
		valid_options = ['y', 'yes', 'n', 'no']
		while True:
			selection=raw_input("\t").strip()
			if selection in valid_options:
				break
			else:
				print("\ntoo big fingers :( wrong command. try again! :)")
		if selection == 'y' or selection ==  'yes':
			adv_wiz_FLAG=True
		if selection == 'n' or selection == 'no':
			adv_wiz_FLAG=False

		if adv_wiz_FLAG==True:
			while True:
				dma = raw_input("\nLED DMA you will use in your system? [default: 10]\t\t\t")
				if (dma.isdigit()==False) or (int(dma) <0):
					print("\nPlease enter correct value!")
				else:
					os.system("sed -i 's/\"LED_DMA\": 10/\"LED_DMA\": "+dma+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				freq = raw_input("\nWhat LED frequency will you use? [default: 800000 - you can type 'def']\t")
				if ((freq.isdigit()==False) or (int(freq) <0) or (int(freq) > 800000)) and (freq != 'def'):
					print("\nPlease enter correct value!")
				elif freq == 'def':
					break
				else:
					os.system("sed -i 's/\"LED_FREQ_HZ\": 800000/\"LED_FREQ_HZ\": "+str(freq)+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				debug_mode = raw_input("\nWill you use RotorHazard in debug mode? [yes/no | default: no]\t\t")
				debug_mode_allowed_values = ['yes','no','1','0','y','n']
				if not debug_mode in debug_mode_allowed_values:
					print("\nPlease enter correct value!")
				else:
					if debug_mode in ['yes','1','y']:
						debug = 'true'
					elif debug_mode in ['no','0','n']:
						debug = 'false'
					os.system("sed -i 's/\"DEBUG\": false/\"DEBUG\": "+str(debug)+"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break
			while True:
				cores = raw_input("\nHome many cores will be available for hosts? [1/2/3/all | default: all]\t")
				cores_values_allowed = ['1','2','3','4','all','*']
				if not cores in cores_values_allowed:
					print("\nPlease enter correct value!")
				else:
					if cores in ['1','2','3']:
						cores_val = str(cores)
						os.system("sed -i 's/\"CORS_ALLOWED_HOSTS\": \"\*\"/\"CORS_ALLOWED_HOSTS\": \""+str(cores_val)+"\"/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					elif cores == 'all':
						cores_val='all'
					else:
						cores_val='*'
					break
			while True:
				serial_ports = raw_input("\nWhich serial ports will you use? [default: 'none']\t\t\t").strip()
				if serial_ports in ['none','0','no']:
					break
				else:
					os.system("sed -i 's/\"SERIAL_PORTS\": [],/\"SERIAL_PORTS\": ["+str(serial_ports)+"],/g' /home/"+user+"/RH-ota/.wizarded-rh-config.json")
					break

		if adv_wiz_FLAG==False:
			debug = 'no'
			cores_val = 'all'
			serial_ports = 'none'
			dma = '10'
			freq = '800000'
			print("\nAdvanced configuration set to default values.\n\n")
			sleep(1.2)

		print("""\n\n\t\t\t"""+bcolors.UNDERLINE+"""CONFIGURATION"""+bcolors.ENDC+""":\n\t
		Admin name: \t\t"""+admin_name+"""
		Admin password: \t"""+admin_pass+"""
		RotorHazard port: \t"""+port+"""
		LED amount: \t\t"""+led_count+"""
		LED pin: \t\t"""+led_pin+"""
		LED inverted: \t\t"""+led_inv+"""
		LED channel: \t\t"""+led_channel+"""
		LED panel rotate: \t"""+panel_rot+"""
		LED rows inverted: \t"""+inv_rows+"""
		LED DMA: \t\t"""+dma+"""
		LED frequency: \t\t"""+freq+"""
		Debug mode: \t\t"""+debug+"""
		Cores allowed: \t\t"""+cores_val+"""
		Serial ports: \t\t"""+serial_ports+"""
		
		\n\n""")
		print("Please check. Confirm? [yes/change/abort]\n")
		valid_options = ['y', 'yes', 'n', 'no', 'change', 'abort']
		while True:
			selection=raw_input().strip()
			if selection in valid_options:
				break
			else:
				print("\ntoo big fingers :( wrong command. try again! :)")
		if selection == 'y' or selection ==  'yes':
			os.system("mv .wizarded-rh-config.json /home/"+user+"/RotorHazard/src/server/config.json")
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

