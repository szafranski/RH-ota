#!/bin/bash

sudo cp /etc/rc.local /etc/rc.local.iptables1_saved

sudo sed -i 's/exit 0//' /etc/rc.local

sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables -A PREROUTING -t nat -p tcp --dport 8080 -j REDIRECT --to-ports 80
sudo iptables-save

echo "
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables -A PREROUTING -t nat -p tcp --dport 8080 -j REDIRECT --to-ports 80

sudo iptables-save
exit 0
" | sudo tee -a /etc/rc.local

green="\033[92m"
red="\033[91m"
endc="\033[0m"
under="\033[4m"
orange="\033[33m"
blue="\033[94m"

printf "

$blue
port forwarding added - server available on default port 80
no need to type server port number in a browser address bar
just type RotorHazard server IP address (probably: $under$(hostname -I | awk '{ print $1 }')$endc$blue)$endc
$orange(services that run on port 80 are available on port 8080 now)$endc"