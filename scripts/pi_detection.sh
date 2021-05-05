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

automatic_pi_detection() {
  ifs=':' read -ra piversion <<<"$(cat /proc/cpuinfo | grep Revision)"
  if [[ ${piversion[2]} == *"90009"* || ${piversion[2]} == *"9000c"* || ${piversion[2]} == *"92009"* ]]; then
    pi_zero_found=true
    echo 'pi zero chipset'
  elif [[ ${piversion[2]} == *"0311"*  ]]; then
    pi_4_found=true
    echo 'pi 4 chipset'
  else
    generic_pi_found=true
    echo 'generic pi chipset'
  fi
}

green="\033[92m"
red="\033[91m"
endc="\033[0m"

pi_detection_error() {
  printf "
     $red -- automatic Pi version detection error -- $endc

  Please make sure that interfaces like SPI, I2C and UART
  were enabled properly using $green sudo raspi-config$endc.

  Hit 'Enter' to continue

  "
  read -r _
  sleep 2
}

automatic_pi_detection || pi_detection_error