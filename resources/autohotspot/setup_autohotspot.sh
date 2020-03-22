#!/bin/bash

#This script was created from : https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/158-raspberry-pi-auto-wifi-hotspot-switch-direct-connection
#it should be everything needed to setup a raspberry pi with wifi support to auto switch between 
#being a wifi hotspot, and connecting to known networks. 

sudo apt-get update
sudo apt-get upgrade
#host access point daemon
sudo apt-get install hostapd
#DNS mask 
sudo apt-get install dnsmasq

#Disable automatic hotspot at startup
#which was setup during install of last two items
sudo systemctl unmask hostapd
sudo systemctl disable hostapd
sudo systemctl disable dnsmasq

#copy our access point config into place.
sudo cp -f hostapd.conf /etc/hostapd/hostapd.conf

#change the  name of the hotspot (in place)
echo "What do you want your hotspot name to be (default is ROTORHAZARD):"
read -r hotspot

if [[ -n "${hotspot}" ]]; then
  sudo sed -i.bak "s/ROTORHAZARD/${hotspot}/" /etc/hostapd/hostapd.conf
fi

#change the  password of the hotspot (in place)
echo "what do you want your hotspot password to be (default is PASSWORD):"
read -r password
if [[ -n "${password}" ]]; then
  sudo sed -i.bak "s/PASSWORD/${password}/" /etc/hostapd/hostapd.conf
fi


#switch daemon to our config
#uncomment DAEMON_CONF and set it to our hostapd.conf
#Comment DAEMON_OPTS="" to #DAEMON_OPTS=""
if grep -q '#DAEMON_CONF=' "/etc/default/hostapd"; then
  sudo sed -i.bak 's:#DAEMON_CONF="":DAEMON_CONF="/etc/hostapd/hostapd.conf":g' /etc/default/hostapd
  sudo sed -i.bak 's:^DAEMON_OPTS="":#DAEMON_OPTS="":g' /etc/default/hostapd
else
  echo DAEMON_CONF already set.
fi

#append the autohotspot config to dnsmasq.conf
if grep -q '#AutoHotspot Config' "/etc/dnsmasq.conf"; then
  echo autohotspot already configured in /etc/dnsmasq.conf
else
  sudo cat autohotspot_dnsmasq.conf | tee -a /etc/dnsmasq.conf
fi

#Clear out network interfaces file:
sudo mv /etc/network/interfaces "/etc/network/interfaces-backup-$(date)"
sudo cp interfaces.conf /etc/network/interfaces

if grep -q 'nohook wpa_supplicant' "/etc/dhcpcd.conf"; then
  echo nohook wpa_supplicant already set.
else
  sudo printf 'nohook wpa_supplicant' | tee -a /etc/dhcpcd.conf
fi
#Configure the actual autohotspot service
sudo cp -f autohotspot.service /etc/systemd/system/autohotspot.service
sudo systemctl enable autohotspot.service

#Create the autohotspot command
sudo cp -f autohotspot /usr/bin/autohotspot
#Make it executable
sudo chmod +x /usr/bin/autohotspot
