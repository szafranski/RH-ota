#!/bin/bash

echo " -- attempt to fix the nameserver --
"
cat /etc/resolv.conf
echo "changing to: "
sudo mv /etc/resolv.conf /etc/resolv.conf.orig
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
echo "old nameserver is saved as: /etc/resolv.conf.orig"
sudo chmod o+r /etc/resolv.conf
echo "
 -- nameserver fixed --
"
sleep 2
