from time import sleep

import os

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



myPlace = data['country']   ### change accordingly




def image():

	print("""

\t\t                               **/(((/**                              

\t\t                            */###########(*                           

\t\t                          */#####@@@@@#####(*                         

\t\t                         *(((((@@@###@@@#####*,                       

\t\t                       */((((@@@#######@@@####/*                      

\t\t                      *(((((@@@(((((#(##@@@#####*                     

\t\t                    **((((&@@&((((*...####@@@####**                   

\t\t                   *(((((@@@((((((....((((#@@@#####*                  

\t\t                 **((((#@@@((((((*.....((((#%@@&####/*                

\t\t                */((((@@@((((((((......(((((((@@@####(*               

\t\t              .*(((((@@@(((((((((......((((((((@@@%####**             

\t\t             */((((@@@(((((((((((......((((((((((@@@####(*            

\t\t            *(((((@@@((((((((((((.....*(((((((((((@@@#####*,          

\t\t          **((((@@@((((((((((((((.....((((((((((((((@@@(#(#/*         

\t\t          *((((@@@(((((((((((((((.....(((((((((((((((@@@((###*        

\t\t       */((((&@@&(((((((((((((,...(((....(((((((((((((#@@@((((/*      

\t\t      */((((@@@(((((((((......................((((((((((@@@((((#*     

\t\t    .*//(((@@@((((((............(((((((*.........,(((((((%@@&((((/*   

\t\t   */////@@@(((((........../((((((((((((((*..........((((((@@@(((((*  

\t\t  */////@@@/(((......./(((((((((((((((((((((((/......../((((@@@#((((*.

\t\t *////%@@/////(((((((((((((((((((((((((((((((((((((((..(((((((@@@((((*

\t\t *////@@@/////////((((((((((((((((((((((((((((((((((((((((((((@@@((((*

\t\t **/////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((**

\t\t  ***/////////////////(((((((((((((((((((((((((((((((((((((((((((((** 

\t\t     ****////////////////((((((((((((((((((((((((((((((((((((/****   

""")



def logo():

	print("""\n	

		#######################################################################

		###                                                                 ###

		###                        """+bcolors.ORANGE+"""RotorHazard"""+bcolors.ENDC+"""                              ###

		###                                                                 ###

		###                   OTA Updater and Manager                       ###

		###                                                                 ###

		#######################################################################""")



def first ():

	image ()

	os.system("clear")

	print("\n\n")

	image()

	sleep(1.3)

first()


# Set the WiFi country in raspi-config's Localisation Options:

# sudo raspi-config

# ( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )


print("""Step 1.""")

def stepOne():
	os.system("sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf")
	os.system("echo 'country="+myPlace+"'| sudo  tee -a /boot/config.txt")
	os.system("sudo apt-get update && sudo apt-get upgrade -y")
	os.system("curl -sL https://install.raspap.com | bash -s -- -y")
	print("""\n\t\t\t\t"""+bcolors.GREEN+"""    Reboot by pressing 'r' """+bcolors.ENDC+"""\n\n\t\t\t\t"""
			+bcolors.YELLOW+"""    Go back by pressing 'b'"""+bcolors.ENDC+"""\n\n""")
			selection=str(raw_input(""))
			if selection=='r':
				os.system("sudo reboot")
			if selection=='b':
				featuresMenu()
			else :
				apManager()

def stepTwo:
	print("""Step 2.""")

	print("""
connect PC to WiFi network: <br/>
name: raspi-webgui<br/>
password: ChangeMe<br/><br/><br/>

enter IP address: 10.3.141.1 in browser

Username: admin

Password: secret<br/>  <br/>

Click:
Configure hotspot -> SSID (enter name you want, eg. "RH-TIMER") 

Wireless Mode (change to 802.11n - 2.4GHz)

save settings  
<br/>
<br/>

Click:
Configure hotspot -> security tab

PSK (enter password that you want to have, eg. "timerpass")

save settings
<br/>

DON'T CHANGE OTHER SETTINGS IN GUI!  
<br/>
<br/>

""")

def stepThree():

	print("""Step 3.""")

	os.system("sudo mv /etc/dhcpcd.conf /etc/dhcpcd.conf.orig")
	os.system("echo 'interface wlan0' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static ip_address=10.10.10.10/24' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static routers=10.10.10.10' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo ' ' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'interface eth0' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static ip_address=172.20.20.20/20' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static routers=172.20.20.20' | sudo tee -a /etc/dhcpcd.conf")
	os.system("echo 'static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf")
	os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.my")
	os.system("sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.netap")
	os.system("sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig")
	os.system("echo 'interface=wlan0' | sudo tee -a /etc/dnsmasq.conf")
	os.system("echo 'dhcp-range=10.10.10.11,10.10.10.255,255.255.255.0,24h' | sudo tee -a /etc/dnsmasq.conf")
	os.system("echo ' ' | sudo tee -a /etc/dnsmasq.conf")
	os.system("echo 'interface=eth0' | sudo tee -a /etc/dnsmasq.conf")
	os.system("echo 'dhcp-range=172.20.20.21,172.20.20.255,255.255.255.0,24h' | sudo tee -a /etc/dnsmasq.conf")
	os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.my")
	os.system("sudo reboot")

def stepFour():

	print("""Step 4.""")

print("""
Connect PC to WiFi network:
name: RH-TIMER
password: timerpass
if you have any problems connecting wifi with new name - try "forgetting" the (old) network in PC's WiFi settings and than try again

Now you should be able to enter the network typing in the browser:
10.10.10.10:5000 - using WiFi
172.20.20.20:5000 - using ethernet.
""")

def stepFive():

	print("""Step 5.""")
	os.system("echo 'interface wlan0' | sudo tee -a /etc/dhcpcd.conf.net")
	os.system("echo 'static ip_address=10.10.10.10/24' | sudo tee -a /etc/dhcpcd.conf.conf.net")
	os.system("echo 'static routers=10.10.10.10' | sudo tee -a /etc/dhcpcd.conf.conf.net")
	os.system("echo 'static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf.conf.net")
	os.system("echo ' ' | sudo tee -a /etc/dhcpcd.conf.net")
	os.system("echo 'interface eth0' | sudo tee -a /etc/dhcpcd.conf.net")
	os.system("echo '#static ip_address=172.20.20.20/20' | sudo tee -a /etc/dhcpcd.conf.net")
	os.system("echo '#static routers=172.20.20.20' | sudo tee -a /etc/dhcpcd.conf.net")
	os.system("echo '#static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf.net")

def apConf():
	os.system("sudo cp /etc/dhcpcd.netap /etc/dhcpcd.conf")
	os.system("sudo reboot") ok?

def netConf():
	os.system("sudo cp /etc/dhcpcd.netap /etc/dhcpcd.conf")
	os.system("sudo reboot") ok?
