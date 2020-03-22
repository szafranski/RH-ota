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

#switch daemon to our config
#uncomment DAEMON_CONF and set it to our hostapd.conf
#Comment DAEMON_OPTS="" to #DAEMON_OPTS=""
sudo sed 's:#DAEMON_CONF="":DAEMON_CONF="/etc/hostapd/hostapd.conf":g' /etc/default/hostapd
sudo sed 's:^DAEMON_OPTS="":#DAEMON_OPTS="":g' /etc/default/hostapd

#append the autohotspot config to dnsmasq.conf
sudo cat autohotspot_dnsmasq.conf >> /etc/dnsmasq.conf

#Clear out network interfaces file:
sudo cp /etc/network/interfaces /etc/network/interfaces-backup
sudo cp interfaces.conf /etc/network/interfaces

sudo printf 'nohook wpa_supplicant' >> /etc/dhcpcd.conf

#Configure the actual autohotspot service
sudo cp autohotspot.service /etc/systemd/system/autohotspot.service
sudo systemctl enable autohotspot.service

#Create the autohotspot command
sudo cp autohotspot /usr/bin/autohotspot
#Make it executable
sudo chmod +x /usr/bin/autohotspot
