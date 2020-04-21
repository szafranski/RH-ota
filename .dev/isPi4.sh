#!/bin/bash

ifs=':' read -ra piversion <<< "$(cat /proc/cpuinfo | grep Revision)"
if [[ ${piversion[2]} == *"0311"* ]] ; then
echo "Pi 4 detected - no errors" || echo " -- error 1 -- "
else
echo "This is not Pi 4 - no errors" || echo " -- error 2 -- "
fi

echo " Thanks for helping!   "