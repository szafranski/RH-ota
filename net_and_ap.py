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

def logoTop():
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

os.system("sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf")
os.system("echo 'country="+myPlace+"'| sudo  tee -a /boot/config.txt")

os.system("sudo apt-get update && sudo apt-get upgrade -y")
os.system("curl -sL https://install.raspap.com | bash -s -- -y")
os.system("sudo reboot") ok?

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


os.system("echo 'interface wlan0' | sudo tee -a /etc/dhcpcd.conf.net")
os.system("echo 'static ip_address=10.10.10.10/24' | sudo tee -a /etc/dhcpcd.conf.conf.net")
os.system("echo 'static routers=10.10.10.10' | sudo tee -a /etc/dhcpcd.conf.conf.net")
os.system("echo 'static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf.conf.net")
os.system("echo ' ' | sudo tee -a /etc/dhcpcd.conf.net")
os.system("echo 'interface eth0' | sudo tee -a /etc/dhcpcd.conf.net")
os.system("echo '#static ip_address=172.20.20.20/20' | sudo tee -a /etc/dhcpcd.conf.net")
os.system("echo '#static routers=172.20.20.20' | sudo tee -a /etc/dhcpcd.conf.net")
os.system("echo '#static domain_name_server=1.1.1.1 8.8.8.8' | sudo tee -a /etc/dhcpcd.conf.net")

Access point:
os.system("sudo cp /etc/dhcpcd.netap /etc/dhcpcd.conf")
os.system("sudo reboot") ok?

Ext. net:
os.system("sudo cp /etc/dhcpcd.netap /etc/dhcpcd.conf")
os.system("sudo reboot") ok?