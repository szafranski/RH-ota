# from time import sleep
# import os
# import platform
# import sys
# import json
# import subprocess

with open('./net_ap/net_steps.txt', 'rt') as f:
	for line in f:
		if '### step2' in line:
			for line in f:
				print line.replace('\n', '').replace('####', '')
				if '####' in line:
					break