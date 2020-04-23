#!/bin/bash

# description of codes reported when is_pi_4 function is executed:
#Model and PCB Revision	RAM	Hardware Revision Code from cpu info
#Pi Zero v1.2	512MB	900092
#Pi Zero v1.3	512MB	900093
#Pi Zero W	512MB	9000C1
#Pi 3 Model B	1GB	a02082 (Sony, UK)
#Pi 3 Model B	1GB	a22082 (Embest, China)
#Pi 3 Model B+	1GB	a020d3 (Sony, UK)
#Pi 4	1GB	a03111 (Sony, UK)
#Pi 4	2GB	b03111 (Sony, UK)
#Pi 4	4GB	c03111 (Sony, UK)

#if ./isPi4.sh ; then
# sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1
#fi

is_pi_4(){
ifs=':' read -ra piversion <<< "$(cat /proc/cpuinfo | grep Revision)"
if [[ ${piversion[2]} == *"0311"* ]] ; then
  sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1 || return 1
fi
}

green="\033[92m"
red="\033[91m"
endc="\033[0m"

is_pi_4_error(){
  printf "
     $red -- automatic Pi 4 detection error -- $endc

  If you are using Raspberry Pi 4 please edit file '/boot/config.txt'
  and change line 'core_freq=250' to '#core_freq=250'.

  If you are using any other Pi model please ignore that message.

  Hit 'Enter' to continue
  "
  read -r _
  sleep 2
}

ssh_enabling(){
  sudo systemctl enable ssh || return 1
  sudo systemctl start ssh || return 1
  printf "
     $green -- SSH ENABLED -- $endc
  "
  sleep 3
  return 0
}

ssh_error(){
  printf "
     $red -- SSH enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SSH interface
  than reboot

  Hit 'Enter' to continue
  "
  read -r _
  sleep 2
}

spi_enabling(){
  echo "dtparam=spi=on" | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1
  printf "
     $green -- SPI ENABLED -- $endc
  "
  sleep 3
  return 0
}

spi_error(){
  printf "
     $red -- SPI enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable SPI interface
  than reboot

  Hit 'Enter' to continue
  "
  read -r _
  sleep 2
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
  is_pi_4 || is_pi_4_error
  printf "
     $green -- I2C ENABLED -- $endc
     "
  sleep 3
  return 0
}

i2c_error(){
  printf "
     $red -- I2C enabling error -- $endc

  try manual enabling with 'sudo raspi config' later
  please: disable end re-enable I2C interface
  than reboot

  Hit 'Enter' to continue
  "
  read -r _
  sleep 2
}

uart_enabling(){
  echo 'enable_uart=1'| sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt || return 1
  printf "
     $green -- UART ENABLED -- $endc
     "
  sleep 3
  return 0
}

uart_error(){
  printf "
     $red -- UART enabling error -- $endc

  try manual enabling with 'sudo raspi config'
  please: disable end re-enable UART interface
  than reboot

  Hit 'Enter' to continue
  "
  read -r _
  sleep 2
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
  ssh_enabling || ssh_error
  spi_enabling || spi_error
  i2c_enabling || spi_error
  uart_enabling || uart_error
fi
