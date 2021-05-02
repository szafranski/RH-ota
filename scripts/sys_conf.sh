#!/bin/bash

# description of codes reported when is_pi_4 function is executed:
#Model and PCB Revision	RAM	Hardware Revision Code from cpu info
#Code	Model	Revision	RAM	Manufacturer
#900021	A+	1.1	512MB	Sony UK
#900032	B+	1.2	512MB	Sony UK
#900092	Zero	1.2	512MB	Sony UK
#900093	Zero	1.3	512MB	Sony UK
#9000c1	Zero W	1.1	512MB	Sony UK
#9020e0	3A+	1.0	512MB	Sony UK
#920092	Zero	1.2	512MB	Embest
#920093	Zero	1.3	512MB	Embest
#900061	CM	1.1	512MB	Sony UK
#a01040	2B	1.0	1GB	Sony UK
#a01041	2B	1.1	1GB	Sony UK
#a02082	3B	1.2	1GB	Sony UK
#a020a0	CM3	1.0	1GB	Sony UK
#a020d3	3B+	1.3	1GB	Sony UK
#a02042	2B (with BCM2837)	1.2	1GB	Sony UK
#a21041	2B	1.1	1GB	Embest
#a22042	2B (with BCM2837)	1.2	1GB	Embest
#a22082	3B	1.2	1GB	Embest
#a220a0	CM3	1.0	1GB	Embest
#a32082	3B	1.2	1GB	Sony Japan
#a52082	3B	1.2	1GB	Stadium
#a22083	3B	1.3	1GB	Embest
#a02100	CM3+	1.0	1GB	Sony UK
#a03111	4B	1.1	1GB	Sony UK
#b03111	4B	1.1	2GB	Sony UK
#b03112	4B	1.2	2GB	Sony UK
#b03114	4B	1.4	2GB	Sony UK
#c03111	4B	1.1	4GB	Sony UK
#c03112	4B	1.2	4GB	Sony UK
#c03114	4B	1.4	4GB	Sony UK
#d03114	4B	1.4	8GB	Sony UK
#c03130	Pi 400	1.0	4GB	Sony UK

#if ./isPi4.sh ; then
# sed -i 's/core_freq=250/#core_freq=250/' /boot/config.txt > /dev/null 2>&1
#fi

is_pi_4() {
  ifs=':' read -ra piversion <<<"$(cat /proc/cpuinfo | grep Revision)"
  if [[ ${piversion[2]} == *"0311"* ]]; then
    pi_4_found=true
    else
    pi_4_found=false
  fi
}

green="\033[92m"
red="\033[91m"
endc="\033[0m"

is_pi_4_error() {
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

ssh_enabling() {
  sudo systemctl enable ssh || return 1
  sudo systemctl start ssh || return 1
  printf "
     $green -- SSH ENABLED -- $endc


  "
  sleep 3
  return 0
}

ssh_error() {
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

spi_enabling() {
  echo "
  [RH-OTA SPI enabled]
  dtparam=spi=on" | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1
  printf "
     $green -- SPI ENABLED -- $endc


  "
  sleep 3
  return 0
}

spi_error() {
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

i2c_enabling() {
  is_pi_4 || is_pi_4_error
 if [ "$pi_4_found" = true ] ; then
    printf "Raspberry Pi 4 chipset found"
    #sudo sed -i 's/dtparam=i2c/#dtparam=i2c/' /boot/config.txt || return 1
    echo "
    [RH-OTA I2C enabled]
    dtparam=i2c_arm=on
  " | sudo tee -a /boot/config.txt || return 1

else
  echo "
  [RH-OTA I2C enabled]
dtparam=i2c_baudrate=75000
core_freq=250
i2c-bcm2708
i2c-dev
dtparam=i2c1=on
dtparam=i2c_arm=on
  " | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf || return 1

  fi
  printf "
     $green -- I2C ENABLED -- $endc


     "
  sleep 3
  return 0
}

i2c_error() {
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

uart_enabling() {
  sudo cp /boot/cmdline.txt /boot/cmdline.txt.dist
  sudo cp /boot/config.txt /boot/config.txt.dist
  echo "
  [RH-OTA UART enabled]
  enable_uart=1
  " | sudo tee -a /boot/config.txt || return 1
  sudo sed -i 's/console=serial0,115200//g' /boot/cmdline.txt || return 1
  printf "
     $green -- UART ENABLED -- $endc


     "
  sleep 3
  return 0
}

uart_error() {
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

reboot_message() {
  echo "

  Process completed. Please reboot Raspberry now.

  "
}

if [ "${1}" = "all" ]; then
  ssh_enabling || ssh_error
  spi_enabling || spi_error
  i2c_enabling || i2c_error
  uart_enabling || uart_error
fi
