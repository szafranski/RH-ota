from time import sleep
import os

'''
totally personal use program with stupid functions useful only for me
and probably one person on the world - is it you stranger?
'''

terminal_used = 'xterm'  # may be changed to 'default' - not recommended

slow_pc = 0  # change to 1 if you have PC based on Core 2 Duo etc.

pi_user = 'pi'  # username on the pi
ip_first = '10.42.0.'
port = 22  # default port used for ssh

pi_pswd = 'raspberry'


# phrase=pi_user+"@"+10.42.0.245's password :"


def main():
    while True:
        no_search_flag = False
        ip_est_range = input("What range you expect it to be? 1/2/3/4 ")
        if ip_est_range == '1':
            ip_est_start = 2
            ip_est_end = 100
            break
        elif ip_est_range == '2':
            ip_est_start = 101
            ip_est_end = 200
            break
        elif ip_est_range == '3':
            ip_est_start = 201
            ip_est_end = 55
            break
        elif ip_est_range == '4':
            ip_est_start = 245
            ip_est_end = 245
            no_search_flag = True
            break
        else:
            print("again!")

    if not no_search_flag:
        for i in range(ip_est_start, ip_est_end):
            print("testing connection with IP " + str(ip_first) + str(i))
            if terminal_used == 'default':
                os.system("x-terminal-emulator -e ssh " + pi_user + "@" + ip_first + str(i) + " &")
            else:
                os.system("xterm -e ssh " + pi_user + "@" + ip_first + str(i) + " &")
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
    else:
        os.system("xterm -e ssh pi@10.42.0.245 &")


if __name__ == "__main__":
    main()
