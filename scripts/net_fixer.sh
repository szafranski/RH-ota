#!/bin/bash

echo " -- attempt to fix the nameserver --
"
sudo rm /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
sudo chmod o+r /etc/resolv.conf
echo " -- nameserver fixed --
"