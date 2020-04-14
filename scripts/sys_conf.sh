#!/bin/bash

#if ./isPi4.sh ; then
# sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1
#fi
# todo shows error "isPi4... not found" - commented out temporary
# can be implement into this file instead

ssh_enabling(){
  sudo systemctl enable ssh
  sudo systemctl start ssh
}

ssh_error(){
  echo "
     -- SSH enabling error --

  try manual enabling with 'sudo raspi config' later

  Hit 'Enter' to continue
"
read var
}


spi_enabling(){
  echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
}

spi_error(){
  echo "
     -- SPI enabling error --

  try manual enabling with 'sudo raspi config' later

  Hit 'Enter' to continue
  "
read var
}

i2c_enabling(){
  echo "dtparam=i2c_baudrate=75000
core_freq=250
i2c-bcm2708
i2c-dev
dtparam=i2c1=on
dtparam=i2c_arm=on
" | sudo tee -a /boot/config.txt
  sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
}

i2c_error(){
  echo "
     -- I2C enabling error --

  try manual enabling with 'sudo raspi config' later

  Hit 'Enter' to continue
  "
read var
}

uart_error(){
  echo "
     -- UART enabling error --

  try manual enabling with 'sudo raspi config'
  "
  sleep 3
}

if [ "${1}" = "ssh" ]; then
  ssh_enabling
fi

if [ "${1}" = "spi" ]; then
  spi_enabling
fi

if [ "${1}" = "i2c" ]; then
  i2c_enabling
fi

reboot_message(){
  echo "

  Process completed. Please reboot Raspberry now.

  "
}


if [ "${1}" = "all" ]; then
  ssh_enabling || ssh_error
  spi_enabling || spi_error
  i2c_enabling || i2c_error
fi

