import os
from modules import check_if_string_in_file, load_config, copy_file
from pathlib import Path


def main():
    home_dir = os.path.expanduser('~')
    Path(f"{home_dir}/.ota_markers").mkdir(exist_ok=True)

    def aliases_clean():
        if check_if_string_in_file(f'{home_dir}/.bashrc', '### Shortcuts'):
            os.system("sed -i '/# #/d' ~/.bashrc")  # removes lines containing # #
            os.system("perl -i.bak -ne 'print if //../Shortcuts/ or !$x{$_}++' ~/.bashrc")
            # Removes doubled and blank lines after word Shortcuts
            os.system(". ./open_scripts.sh; aliases_clean")  # removes most of old aliases completely
    aliases_clean()


# removes old aliases, especially doubled ones and bad leftovers from ~/.bashrc file
# part of action is done in script - has to be ported


if __name__ == "__main__":
    main()
