from time import sleep
import os
import sys

def main():
	os.system("clear")
	print("\n\t\tThis script would automatically install RotorHazard software on your raspberry. After rebooting please check")
	print("\n\t\tby typing 'sudo raspi-config' if I2C, SPI and SSH protocols are active. Enjoy!")
	print("\n\n\n\t\t Ready - press 'k'")
	selection=str(raw_input(""))
	if selection =='k':	
		os.chdir("/home/pi")
		os.system(" sudo apt-get update && sudo apt-get upgrade -y")
		os.system("sudo systemctl enable ssh")
		os.system("sudo systemctl start ssh ")
		os.system("sudo apt-get install wget python-dev python-rpi.gpio libffi-dev python-smbus build-essential python-pip git scons swig -y")
		os.system("sudo pip install cffi ")
		os.system("echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt")
		os.system("echo 'core_freq=250' | sudo tee -a /boot/config.txt")
		os.system("echo 'dtparam=spi=on' | sudo sudo tee -a /boot/config.txt  ")  
		os.chdir("/home/pi")
		os.system(" wget https://codeload.github.com/RotorHazard/RotorHazard/zip/master -O temp.zip")
		os.system(" unzip temp.zip")
		os.system(" rm temp.zip")
		os.system(" mv RotorHazard-master /home/pi/RotorHazard")
		os.system(" sudo pip install -r /home/pi/RotorHazard/src/server/requirements.txt")
		os.system(" sudo chmod 777 /home/pi/RotorHazard/src/server")
		os.chdir("/home/pi")
		os.system(" sudo git clone https://github.com/jgarff/rpi_ws281x.git")
		os.chdir("/home/pi/rpi_ws281x")
		os.system(" sudo scons")
		os.chdir("/home/pi/rpi_ws281x/python")
		os.system(" sudo python setup.py install")
		os.chdir("/home/pi")
		os.system(" sudo git clone https://github.com/chrisb2/pi_ina219.git")
		os.chdir("/home/pi/pi_ina219")
		os.system(" sudo python setup.py install")
		os.chdir("/home/pi")
		os.system(" sudo git clone https://github.com/rm-hull/bme280.git")
		os.system("/home/pi/bme280")
		os.system(" sudo python setup.py install")
		os.system(" sudo apt-get install openjdk-8-jdk-headless -y")
		os.system(" sudo cp service_file.txt /lib/systemd/system/rotorhazard.service")
		os.system(" sudo chmod 644 /lib/systemd/system/rotorhazard.service")
		os.system(" sudo systemctl daemon-reload")
		os.system(" sudo systemctl enable rotorhazard.service")
		print("\n\n\t\tInstallation completed")
		def end():
			print("\n\n\n\nPlease type 'r' to reboot - recommended - or 'e' to exit")
			def endMenu():
				selection=str(raw_input(""))
			
				if selection =='r':	
					os.system(" sudo reboot")
				if selection =='e':	
					print("\n\n\t\tBye, bye\n\n\t\t")
					sleep(2)
					os.system("clear")
					sys.exit()
				else: 
					end()
			endMenu()	
		end()
	else :
		main()
main()
