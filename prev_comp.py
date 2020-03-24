import os
from modules import check_if_string_in_file, load_config, copy_file
from pathlib import Path


# if os.stat(home_dir+'/.ota_markers/ota_config.txt').st_size == 0:
#    os.system("rm {home_dir}/.ota_markers/ota_config.txt > /dev/null 2>&1")


def main():
    # parser, config = load_config()
    home_dir = os.path.expanduser('~')
    Path(f"{home_dir}/.ota_markers").mkdir(exist_ok=True)

    # prev_comp(parser, home_dir)
    def aliases_clean():
        if check_if_string_in_file(f'{home_dir}/.bashrc', '### Shortcuts'):
            os.system(". ./open_scripts.sh; aliases_clean")

    aliases_clean()

# tried to remove lines from 'Shortcut' to 'After'

# removes old aliases, especially doubled ones from ~/.bashrc file


# We create a main method to capture the context for any variables
# we want to build in this script when running standalone.
#
# main() is only called if you run this script from the command line directly eg:
# python3 prev_comp.py
#
# it will NOT be called if you import this file into another file.


if __name__ == "__main__":
    main()
