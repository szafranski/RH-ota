#!/bin/bash

# possible RTC models

# ds1307
# pcf8523
# ds3231
echo
dtoverlay=i2c-rtc,"${1}" | sudo tee -a /boot/config.txt
echo

sudo apt-get -y remove fake-hwclock
sudo update-rc.d -f fake-hwclock remove
sudo systemctl disable fake-hwclock

# todo comment out those lines 2 and 3 below only when they are right below that first below - waiting for Clayton
sed -i 's/if [ -e \/run\/systemd\/system ] ; then/#if [ -e \/run\/systemd\/system ] ; then/g' /lib/udev/hwclock-set
sed -i 's/if [ -e /run/systemd/system ] ; then/#if [ -e /run/systemd/system ] ; then/g' /lib/udev/hwclock-set
sed -i 's/if [ -e /run/systemd/system ] ; then/#if [ -e /run/systemd/system ] ; then/g' /lib/udev/hwclock-set

sed -i 's/\/sbin\/hwclock --rtc=$dev --systz --badyear/#\/sbin\/hwclock --rtc=$dev --systz --badyear/g' /lib/udev/hwclock-set
sed -i 's/\/sbin\/hwclock --rtc=$dev --systz/#\/sbin\/hwclock --rtc=$dev --systz/g' /lib/udev/hwclock-set

#Comment out those:
#if [ -e /run/systemd/system ] ; then
#exit 0
#fi
#Also comment out the two lines:
#/sbin/hwclock --rtc=$dev --systz --badyear
#/sbin/hwclock --rtc=$dev --systz

#First run date to verify the time is correct. Plug in Ethernet or WiFi to let the Pi sync \
# the right time from the Internet. Once that's done, run sudo hwclock -w to write the time, \
# and another sudo hwclock -r to read the time
sudo hwclock -w
sleep 1
sudo hwclock -r
#Once the time is set, make sure the coin cell battery is inserted so that the time is saved. \
# You only have to set the time once assuming the coin cell doesn't die.
