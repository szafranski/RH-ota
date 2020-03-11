from time import sleep
import os
import platform
import sys

os.system("rm index* > /dev/null 2>&1")
#[ "$(ping -c 2 8.8.8.8 | grep '100% packet loss' )" != "" ]
os.system("wget www.google.com")
os.system("sleep 1")
os.system("exit")