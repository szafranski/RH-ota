#!/bin/bash

ifs=':' read -ra piversion <<< "$(cat /proc/cpuinfo | grep Revision)"
if [[ ${piversion[2]} == *"0311"* ]] ; then
echo "Pi 4 detected - no errors" || echo " -- error 1 -- "
else
echo "This is not Pi 4 - no errors" || echo " -- error 2 -- "
fi

echo " Thanks for helping!   "

#!/bin/bash

#Model and PCB Revision	RAM	Hardware Revision Code from cpuinfo
#Pi Zero v1.2	512MB	900092
#Pi Zero v1.3	512MB	900093
#Pi Zero W	512MB	9000C1
#Pi 3 Model B	1GB	a02082 (Sony, UK)
#Pi 3 Model B	1GB	a22082 (Embest, China)
#Pi 3 Model B+	1GB	a020d3 (Sony, UK)
#Pi 4	1GB	a03111 (Sony, UK)
#Pi 4	2GB	b03111 (Sony, UK)
#Pi 4	4GB	c03111 (Sony, UK)

ifs=':' read -ra piversion <<< "$(cat /proc/cpuinfo | grep Revision)"
if [[ ${piversion[2]} == *"0311"* ]] ; then
  exit 0
else
  exit 1
fi
