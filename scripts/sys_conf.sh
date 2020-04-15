#!/bin/bash

#if ./isPi4.sh ; then
# sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1
#fi
# todo shows error "isPi4... not found" - commented out temporary
# can be implement into this file instead

ssh_enabling(){
  sudo systemctl enable ssh || return 1
  sudo systemctl start ssh || return 1
  echo "
     -- SSH ENABLED --   
  "
  sleep 3
  return 0
}

ssh_error(){
  echo "
     -- SSH enabling error --

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SSH interface
  than reboot 
  
  Hit 'Enter' to continue
  "
  read -r _
}


spi_enabling(){
  echo "dtparam=spi=on" | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1
  echo "
     -- SPI ENABLED --   
  "
  sleep 3
  return 0
}

spi_error(){
  echo "
     -- SPI enabling error --

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SPI interface
  than reboot 
  
  Hit 'Enter' to continue
  "
  read -r _
}

i2c_enabling(){
  echo "dtparam=i2c_baudrate=75000
  core_freq=250
  i2c-bcm2708
  i2c-dev
  dtparam=i2c1=on
  dtparam=i2c_arm=on
  " | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1
  echo "
     -- I2C ENABLED --   
     "
  sleep 3
  return 0
}

i2c_error(){
  echo "
     -- I2C enabling error --

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable I2C interface
  than reboot 
  
  Hit 'Enter' to continue
  "
  read -r _
}

uart_enabling(){
  echo 'enable_uart=1'| sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt || return 1
  echo "
     -- UART ENABLED --   
     "
  sleep 3
  return 0Z
}

uart_error(){
  echo "
     -- UART enabling error --

  try manual enabling with 'sudo raspi config'
  please: disable end re-enable UART interface
  than reboot 
    
  Hit 'Enter' to continue
  "
  read -r _
}

if [ "${1}" = "ssh" ]; then
  ssh_enabling || ssh_error
fi

if [ "${1}" = "spi" ]; then
  spi_enabling || spi_error
fi

if [ "${1}" = "i2c" ]; then
  i2c_enabling || i2c_error
fi

if [ "${1}" = "uart" ]; then
  uart_enabling || uart_error
fi

reboot_message(){
  echo "

  Process completed. Please reboot Raspberry now.

  "
}


if [ "${1}" = "all" ]; then
  ssh_enabling
  spi_enabling
  i2c_enabling
fi

