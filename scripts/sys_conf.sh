#!/bin/bash

sudo systemctl enable ssh
sudo systemctl start ssh
echo "dtparam=i2c_baudrate=75000
core_freq=250
dtparam=spi=on
i2c-bcm2708
i2c-dev
dtparam=i2c1=on
dtparam=i2c_arm=on
" | sudo tee -a /boot/config.txt
sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf

#if ./isPi4.sh ; then
# sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1
#fi
# todo shows error "isPi4... not found" - commented out temporarly