import os
from time import sleep


def main():
    print("\n")
    user_name = input("User name: ").strip()
    print("\n")
    user_code = input("User code: ").strip()
    print("\n")

    os.system(f"rm {user_name}_log_old.txt > /dev/null 2>&1")
    os.system(f"cp {user_name}_log.txt {user_name}_log_old.txt > /dev/null 2>&1")
    os.system(f"curl https://transfer.sh/{user_code}/{user_name}_log.txt -o {user_name}_log.txt")

    sleep(1)

    if os.path.exists(f"./{user_name}_log.txt"):
        print("\n")
        sel = input("Open log file now? [y/n]")
        if sel == 'y':
            os.system(f"less {user_name}_log.txt")
        else:
            pass
    else:
        input("Downloading file - error")


if __name__ == "__main__":
    main()
