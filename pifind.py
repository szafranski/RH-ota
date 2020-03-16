from time import sleep 
import os

selection = str(raw_input("Do you have 'xterm' installed? [hit 'n' if not or 'Enter' to dismiss]\n"))
#selection = str(raw_input("Do you have 'xterm' and 'expect' installed? [hit 'n' if not or any other key to dismiss]\n"))
if selection == 'n':
	print("Please install it now.\n")
	os.system("sudo apt install xterm")
#	os.system("sudo apt install expect")

terminal_used = 'xterm'    ## may be changd to 'default' - not recommended

pi_user = 'pi'                # user name on the pi
ip_first = '10.42.0.'
port = 22                      # default port used for ssh

pi_pwsd='raspberry'

#phrase=pi_user+"@"+10.42.0.245's password :"

for i in range (2, 255):
	print("testing connection with IP "+str(ip_first)+str(i))
	if terminal_used == 'default':
		os.system("x-terminal-emulator -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
	else:
		os.system("xterm -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
	if (i % 50) == 0:
		sleep(2)  # prevens error due to too many xterm instances opened
		print("checking...")
		#os.system("kill -9 $(pidof xterm)")

# for i in range (2, 255):
	# print("testing connection with IP "+str(ip_first)+str(i)+" port "+str(port))
	# os.system("xterm -e ssh "+pi_user+"@"+ip_first+str(i)+" port "+str(port)+" &" )
	# if (i % 50) == 0:
		# sleep(5)
		# print("checking...")
		# #os.system("kill -9 $(pidof xterm)")

