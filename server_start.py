import os
import sys

user = 'pi'

os.chdir("/home/"+user+"/RotorHazard/src/server")
os.system("python server.py")