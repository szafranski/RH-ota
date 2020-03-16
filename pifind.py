from time import sleep 
import os
import sys

terminal_used = 'xterm'    ## may be changd to 'default' - not recommended

slow_pc = 1            # change to 1 if you have PC based on Core 2 Duo etc.

pi_user = 'pi'                 # user name on the pi
ip_first = '10.42.0.'
port = 22                      # default port used for ssh

pi_pwsd='raspberry'

#phrase=pi_user+"@"+10.42.0.245's password :"

selection = str(raw_input("Do you have 'xterm' installed? \n[hit 'n' if not, 'c' - to cancel or 'Enter' to dismiss]\n"))
if selection == 'n':
	print("Please install it now.\n")
	os.system("sudo apt install xterm")
#	os.system("sudo apt install expect")
if selection == 'c':
	sys.exit()

for i in range (2, 255):
	print("testing connection with IP "+str(ip_first)+str(i))
	if terminal_used == 'default':
		os.system("x-terminal-emulator -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
	else:
		os.system("xterm -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
	if (i % 50) == 0:
		if slow_pc == 0:
			sleep(2)  # prevens error due to too many xterm instances opened
		else:
			if (i % 100) == 0:
				print("Waiting due to slow PC option enabled")
				sleep(20)
			if (i % 200) == 0:
				print("Waiting due to slow PC option enabled")
				os.system("kill -9 $(pidof xterm)")
				sleep(20)
			sleep(5)
		print("checking...")

# for i in range (2, 255):
	# print("testing connection with IP "+str(ip_first)+str(i)+" port "+str(port))
	# os.system("xterm -e ssh "+pi_user+"@"+ip_first+str(i)+" port "+str(port)+" &" )
	# if (i % 50) == 0:
		# sleep(5)
		# print("checking...")
		# #os.system("kill -9 $(pidof xterm)")

