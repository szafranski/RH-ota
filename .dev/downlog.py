import os

print("\n")
user_name = input("User name: ").strip()
print("\n")
user_code = input("User code: ").strip()
print("\n")

os.system(f"rm {user_name}_log_old.txt > /dev/null 2>&1")
os.system(f"cp {user_name}_log.txt {user_name}_log_old.txt > /dev/null 2>&1")

os.system(f"curl https://transfer.sh/{user_code} -o {user_name}_log.txt")

while True:
    print("\n")
    sel = input("Open file now? [y/n]")
    if sel == 'y':
        os.system(f"less {user_name}_log.txt")
        break
    if sel == 'n':
        break
    else:
        continue
