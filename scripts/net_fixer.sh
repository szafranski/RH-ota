#!/bin/bash

echo
sudo rm /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
sudo chmod o+r /etc/resolv.conf
printf " -- nameserver fixed -- "