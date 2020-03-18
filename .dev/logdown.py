import os
import sys

print("\n")
user_name = str(raw_input("User name: "))
print("\n")
user_code = str(raw_input("User code: "))
print("\n")

os.system("rm "+user_name+"_log_old.txt > /dev/null 2>&1")
os.system("cp "+user_name+"_log.txt "+user_name+"_log_old.txt > /dev/null 2>&1")

os.system("curl https://transfer.sh/"+user_code+"/"+user_name+"_log.txt -o "+user_name+"_log.txt")

while True:
    print("\n")
    sel = str(raw_input("Open file now? [y/n]"))
    if sel == 'y':
        os.system("less "+user_name+"_log.txt")
        break
    if sel == 'n':
        break
    else:
        continue