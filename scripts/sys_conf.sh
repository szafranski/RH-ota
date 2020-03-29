#!/bin/bash

sudo systemctl enable ssh
sudo systemctl start ssh
echo
echo 'dtparam=i2c_baudrate=75000' | sudo tee -a /boot/config.txt
echo 'core_freq=250' | sudo tee -a /boot/config.txt
echo 'dtparam=spi=on' | sudo sudo tee -a /boot/config.txt
echo 'i2c-bcm2708' | sudo tee -a /boot/config.txt
echo 'i2c-dev' | sudo tee -a /boot/config.txt
echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt
echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt
echo
sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
