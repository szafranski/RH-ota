#!/bin/bash

sudo rfkill unblock wifi # in case of WiFi being still blocked at this point
echo '#[Raspberry as AccessPoint - added by OTA]' | sudo tee -a ~/.bashrc
echo 'alias netcfg="cp /etc/dhcpcd.conf.net /etc/dhcpcd.conf"  # Pi as client' | sudo tee -a ~/.bashrc
echo 'alias apcfg="cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf"  # Pi as AP' | sudo tee -a ~/.bashrc
sudo cp /home/"${1}"/RH_Install-Manager/net_ap/dhcpcd.conf.net /etc/dhcpcd.conf.net
sudo cp /home/"${1}"/RH_Install-Manager/net_ap/dhcpcd.conf.ap /etc/dhcpcd.conf.ap
sudo cp /home/"${1}"/RH_Install-Manager/net_ap/dnsmasq.conf.ap /etc/dnsmasq.conf.ap
sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig
sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
# sudo cp /home/"${1}"/RH_Install-Manager/net_ap/dnsmasq.conf.net /etc/dnsmasq.conf.net
sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.orig
sudo sed -i 's/country/# country/g' /etc/wpa_supplicant/wpa_supplicant.conf
cat /etc/wpa_supplicant/wpa_supplicant.conf | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf.tmp
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
echo country="${1}" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
cat /etc/wpa_supplicant/wpa_supplicant.conf.tmp | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
# echo country="${1}"| sudo tee -a /boot/config.txt
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf.tmp
