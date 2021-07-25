#!/bin/bash


### Raspberry Pi 0 -          BCM2835
### Raspberry Pi 1 -          BCM2835
### Raspberry Pi 2 -          BCM2836/7
### Raspberry Pi 3 B -        BCM2837A0/B0
### Raspberry Pi 3 A+/B+ -    BCM2837A0/B0
### Raspberry Pi 4 -          BCM2711



pi_version=$(echo "$(tr -d '\0' < /proc/device-tree/compatible)" | rev | awk -F"," '{print $1}' | rev | xargs)

if [[ $pi_version == "bcm2835" ]]; then
  echo "pi_zero"
elif [[ $pi_version == "bcm2711" ]]; then
  echo "pi_4"
else
  echo "pi_3_default"
fi


