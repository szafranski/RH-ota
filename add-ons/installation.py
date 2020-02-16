from time import sleep
import os
import sys

os.system("clear")
print("\nThis script would automatically install RotorHazard software on your raspberry. After rebooting please check")
print("\nby typing 'sudo raspi-config' if I2C, SPI and SSH protocols are active. Enjoy!")

print("\n\n\n\t\t Ready - press 'k'n")
selection=str(raw_input(""))
if selection =='k':	
	os.system(" cd ~")
	os.system(" sudo apt-get update && sudo apt-get upgrade -y")

	os.system("echo 'dtparam=spi=on' | /boot/config.txt  ")  

	os.system("sudo systemctl enable ssh")
	os.system("sudo systemctl start ssh ")
	os.system("sudo apt-get install wget python-dev python-rpi.gpio libffi-dev python-smbus build-essential python-pip git scons swig -y")
	os.system("sudo pip install cffi ")

	os.system("echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt  ")    

	os.system("echo 'core_freq=250' | sudo tee -a /boot/config.txt      ")

	os.system(" cd ~")
	os.system(" wget https://codeload.github.com/RotorHazard/RotorHazard/zip/master -O temp.zip")
	os.system(" unzip temp.zip")
	os.system(" mv RotorHazard-master RotorHazard")
	os.system(" rm temp.zip")

	os.system(" cd ~/RotorHazard/src/server")
	os.system(" sudo pip install -r requirements.txt")

	os.system(" cd ~/RotorHazard/src")
	os.system(" sudo chmod 777 server")

	os.system(" cd ~")
	os.system(" sudo git clone https://github.com/jgarff/rpi_ws281x.git")
	os.system(" cd rpi_ws281x")
	os.system(" sudo scons")

	os.system(" cd python")
	os.system(" sudo python setup.py install")

	os.system(" cd ~")
	os.system(" sudo git clone https://github.com/chrisb2/pi_ina219.git")
	os.system(" cd pi_ina219")

	os.system(" sudo python setup.py install")

	os.system(" cd ~")
	os.system(" sudo git clone https://github.com/rm-hull/bme280.git")
	os.system(" cd bme280")

	os.system(" sudo python setup.py install")

	os.system(" sudo apt-get install openjdk-8-jdk-headless -y")

	os.system(" sudo cp service_file.txt /lib/systemd/system/rotorhazard.service")

	os.system(" sudo chmod 644 /lib/systemd/system/rotorhazard.service")

	os.system(" sudo systemctl daemon-reload")
	os.system(" sudo systemctl enable rotorhazard.service")
	print("\n\n\t\tInstallation completed. \n\n\n\nPlease type 'sudo reboot'")
else :
	pass
