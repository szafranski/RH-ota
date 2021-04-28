#!/bin/bash

sudo cp /etc/rc.local /etc/rc.local.save_iptables
sudo sed -i 's/exit 0//' /etc/rc.local

echo "
sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 5000
sudo iptables-save

exit 0
" | sudo tee -a /etc/rc.local

echo "

port forwarding added

"