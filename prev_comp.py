import os
from modules import check_if_string_in_file, load_config, copy_file
from pathlib import Path

# if os.stat(homedir+'/.ota_markers/ota_config.txt').st_size == 0:
#    os.system("rm {homedir}/.ota_markers/ota_config.txt > /dev/null 2>&1")

# def main():

home_dir = '/home/andrzej/'


# Path(f"{home_dir}/.ota_markers").mkdir(exist_ok=True)
def aliases_clean():
    if check_if_string_in_file(f'{home_dir}/.bashrc', '### Shortcuts'):
        # os.system("perl - i.bak - ne 'print if ! $a{$_}++' " + home_dir + ".bashrc")  # removes doubled lines
        os.system(". ./open_scripts.sh; aliases_clean")
        # os.system("sed -i '/# #/d' " + home_dir + ".bashrc")  # removes lines containing # #
        # os.system("grep -n \"Shortcuts\" ~/.bashrc | awk -F  \":\" '{print $1}' > .tmp1")
        # os.system("grep -n \"After \" ~/.bashrc | awk -F  \":\" '{print $1}' > .tmp2")
        # first = 0  # .tmp1
        # last = 0  # .tmp2
        # print("-----------")
        # os.system("rm .tmp1")
        # os.system("rm .tmp2")
        # # os.system(f"sed 'first,last' {home_dir}/.bashrc")


# tried to remove lines from 'Shortcut' to 'After'

# removes old aliases, especially doubled ones from ~/.bashrc file


# main()

'''
We create a main method to capture the context for any variables
we want to build in this script when running standalone. 

main() is only called if you run this script from the command line directly eg:
python3 prev_comp.py

it will NOT be called if you import this file into another file.
'''


def main():
    parser, config = load_config()
    #     home_dir = os.path.expanduser('~')
    # prev_comp(parser, home_dir)
    aliases_clean()


'''
This if statement is responsible for detecting if this script 
was run from command line.  it is only true when this script
is run from the console. 
'''
if __name__ == "__main__":
    main()
