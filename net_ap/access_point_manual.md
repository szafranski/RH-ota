# RH-access_point
additional simple instruction how to make RotorHazard race timer working on raspberry without using external router.

<br/>
Confirmed to work on Raspberry Pi 3 B+ with Raspbian Buster Lite installed.

<br/><br/>

The best moment to do that is after fresh installation of RotorHazard and Raspbian when you still have internet access on your raspberry.<br/><br/> 

<br/> 

Update raspberry - in terminal:<br/> 
(you have to have internet connection)

________________

sudo apt-get update <br/>
sudo apt-get dist-upgrade <br/>
sudo reboot
________________

<br/>

Set the WiFi country in raspi-config's Localisation Options: 

In terminal (SSH):<br/>
sudo raspi-config <br/>
( 4. point -> I4 - Change WiFi country -> select -> enter -> finish )

<br/>

  
In terminal (SSH):
________________

curl -sL https://install.raspap.com | bash -s -- -y
________________

(takes several minutes - if nothing happened in the terminal - you don't have internet access which is required)
________________
sudo reboot + unplug the Ethernet cable if was connected
<br/>

________________
<br/>

connect PC to WiFi network: <br/>
name: raspi-webgui<br/>
password: ChangeMe<br/><br/><br/>





enter IP address: 10.3.141.1 in browser

Username: admin

Password: secret<br/>  <br/>



Click:
Configure hotspot -> SSID (enter name you want, eg. "RH-TIMER") 

Wireless Mode (change to 802.11n - 2.4GHz)

save settings  
<br/>
<br/>

Click:
Configure hotspot -> security tab

PSK (enter password that you want to have, eg. "timerpass")

save settings
<br/>

DON'T CHANGE OTHER SETTINGS IN GUI!  
<br/>
<br/>


In terminal (SSH):

________________

sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.orig

sudo nano /etc/dhcpcd.conf

add at the end of file (or change last lines accordingly):
________________

interface wlan0<br/>
static ip_address=10.10.10.10/24</br>
static routers=10.10.10.10</br>
static domain_name_server=1.1.1.1 8.8.8.8<br/><br/>

interface eth0<br/>
static ip_address=172.20.20.20/20<br/>
static routers=172.20.20.20<br/>
static domain_name_server=1.1.1.1 8.8.8.8
________________

and save (Ctrl+X -> y -> enter)<br/>
<br/>

in terminal (SSH):
<br/> <br/>
sudo cp /etc/dhcpcd.conf /etc/dhcpcd.conf.my

sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig<br/>

sudo nano /etc/dnsmasq.conf

and change the file so it looks like:
________________

interface=wlan0<br/>
  dhcp-range=10.10.10.11,10.10.10.255,255.255.255.0,24h
<br/>

interface=eth0<br/>
  dhcp-range=172.20.20.21,172.20.20.255,255.255.255.0,24h
________________

and save (Ctrl+X -> y -> enter)<br/>

<br/>

In terminal (SSH):

<br/>

sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.my


sudo reboot
<br/>
<br/>

  
Connect PC to WiFi network: <br/>
name: RH-TIMER<br/>
password: timerpass <br/> <br/>
if you have any problems connecting wifi with new name - try "forgetting" the (old) network in PC's WiFi settings and than try again

<br/> <br/>

Now you should be able to enter the network typing in the browser:
10.10.10.10:5000 - using WiFi
172.20.20.20:5000 - using ethernet.

<br/> <br/>

Optional but not recommended:

You can change network name and password entering 10.10.10.10 and logging using: <br/>
Username: admin <br/>
Password: secret <br/>
You can change this logging info as well in Configure Auth in the gui if you want.

<br/> <br/>
<br/> <br/>
Sometimes connecting ethernet cable to any DHCP-server capable device like another router can mess up the configuration.
<br/> <br/>
If for any reasons you would have problems in the future with connecting to the timer - eg. if everything worked well but you entered the RaspAP configuration site, saved some changes (like WiFi password) or you connected raspberry to the router one time etc. and since than you have problems with achieving the connection -  the most probable reason is wrong configuration in 2 files:<br/>
/etc/dhcpcd.conf<br/>
/etc/dnsmasq.conf<br/>

Check those first - connecting with SSH using external router or plug sd card to Linux PC/VM (or Windows using special drivers - cause Windows can't write any changes to ext4 partitions natively) and manually check those.<br/>
If you decide to use external router for troubleshooting - after saving the changes in the files, remember to reboot raspberry.

The easiest way to make sure those files are configured correctly is:
________________

sudo cp /etc/dnsmasq.conf.my /etc/dnsmasq.conf

sudo cp /etc/dhcpcd.conf.my /etc/dhcpcd.conf


Reboot and unplug from the router- if was connected.
________________

<br/>
If you are making any changes in raspberry configuration (changing WiFi password, changing WiFi to 5Ghz - for some reason, changing WiFi country etc.) - always check if everything still works AFTER REBOOTING!

<br/><br/>
!!!!!!!!!!
If you want to have internet connection on your raspberry after this mod check out the file: 
https://github.com/szafranski/RH-access_point/blob/master/internet_connection
