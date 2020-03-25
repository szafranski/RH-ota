from time import sleep 
import os

'''
totally personal use program with stupid functions useful only for me
and probably one person on the world - is it you stranger?
'''

terminal_used = 'xterm'      # may be changed to 'default' - not recommended

slow_pc = 0                  # change to 1 if you have PC based on Core 2 Duo etc.

pi_user = 'pi'               # user name on the pi
ip_first = '10.42.0.'
port = 22                    # default port used for ssh

pi_pswd = 'raspberry'

# phrase=pi_user+"@"+10.42.0.245's password :"

ip_est_start = 0
ip_est_end = 0

while True:
    ip_est_range = input("What range you expect it to be? 1/2/3")
    if ip_est_range == '1':
        ip_est_start = 2
        ip_est_end = 100
        break
    if ip_est_range == '2':
        ip_est_start = 101
        ip_est_end = 200
        break
    if ip_est_range == '3':
        ip_est_start = 201
        ip_est_end = 255
        break
    else:
        print("again!")

for i in range(ip_est_start, ip_est_end):
    print("testing connection with IP "+str(ip_first)+str(i))
    if terminal_used == 'default':
        os.system("x-terminal-emulator -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
    else:
        os.system("xterm -e ssh "+pi_user+"@"+ip_first+str(i)+" &")
    if (i % 50) == 0:
        if slow_pc == 0:
            sleep(2)  # prevents error due to too many xterm instances opened
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

