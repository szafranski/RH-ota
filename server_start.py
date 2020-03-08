from time import sleep
import os
import platform
import sys
import json
import subprocess

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
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

sleep(0.12)
clearTheScreen()
sleep(0.12)
print("\n\n\t\tPlease wait...\n\n")
print("\n")
os.chdir("/home/"+user+"/RotorHazard/src/server")
os.system("python server.py")