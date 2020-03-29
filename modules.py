from pathlib import Path
from shutil import copyfile
from time import sleep
import os
import platform
import sys
import json
import time
import requests  # todo David - no module error, we use it?
from types import SimpleNamespace as Namespace, SimpleNamespace


def clear_the_screen():
    sleep(0.05)
    if platform.system() == "Windows":
        os.system("cls")
    if platform.system() == "Linux":
        os.system("clear")
    else:
        print(("\n" * 200))
    sleep(0.05)


def dots_show(duration):
    for i in range(30):
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(duration / 30)
    sys.stdout.write("\n")


def percent_count():
    def backspace(n):
        sys.stdout.write((b'\x08' * n).decode())  # use \x08 char to go back

    for i in range(101):  # for 0 to 100
        s = str(i) + '%'  # string for output
        sys.stdout.write(s)  # just print
        sys.stdout.flush()  # needed for flush when using \x08
        backspace(len(s))  # back n chars
        time.sleep(0.05)


def image_show():
    with open('./resources/image.txt', 'r') as logo:
        f = logo.read()
        print(f)


def ota_image():
    with open('./resources/ota_image.txt', 'r') as file:
        f = file.read()
        print(f)


def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


def logo_top(linux_testing):
    logo = """
    \n    
    #######################################################################
    ###                                                                 ###
    ###    {orange}{bold}        RotorHazard             {endc}         ###
    ###                                                                 ###
    ###        {bold}        OTA Updater and Manager     {endc}         ###
    ###                                                                 ###
    #######################################################################
    """.format(bold=Bcolors.BOLD_S, endc=Bcolors.ENDC_S,
               yellow=Bcolors.YELLOW_S, orange=Bcolors.ORANGE_S)

    print(logo)
    if linux_testing:
        print("\t\t\t  Linux PC version\t\n")
    sleep(0.05)


class Bcolors:
    HEADER = '\033[95m'
    ORANGE = '\033[33m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    '''
    the following are designed to be used in formatted strings
    they each have enough spaces appended so that {value}
    will be replaced with an equal number of spaces.
    '''
    HEADER_S = '\033[95m' + (' ' * 9)
    ORANGE_S = '\033[33m' + (' ' * 8)
    BLUE_S = '\033[94m' + (' ' * 6)
    GREEN_S = '\033[92m' + (' ' * 7)
    YELLOW_S = '\033[93m' + (' ' * 8)
    RED_S = '\033[91m' + (' ' * 5)
    ENDC_S = '\033[0m' + (' ' * 6)
    BOLD_S = '\033[1m' + (' ' * 6)
    UNDERLINE_S = '\033[4m' + (' ' * 11)


def internet_check():  # too much code - but works for now
    print("""
        Please wait - checking internet connection state....
    """)
    internet_flag = False
    for i in range(3):
        response = requests.get('https://github.com')
        if response.status_code == requests.codes.ok:
            internet_flag = True
            break
    return internet_flag


def load_ota_config(user):
    # .read(f'/home/{config.user}/.ota_markers/ota_config.txt')  # todo remove that line? and only 1 aliases instance
    ota_config_file = f'/home/{user}/.ota_markers/ota_config.json'
    if Path(ota_config_file).exists():
        ota_config = load_json(ota_config_file)
    else:
        ota_config = SimpleNamespace()
        ota_config.serial_added = False
        ota_config.aliases = False
        ota_config.updater_planted = False

    return ota_config


def write_ota_config(ota_config, user):
    ota_config_file = f'/home/{user}/.ota_markers/ota_config.json'
    write_json(ota_config, ota_config_file)


def get_ota_version():  # todo is it ok David?
    this_dir = os.path.dirname(os.path.realpath(__file__))
    with open(f'{this_dir}/version.txt', 'r') as open_file:
        version = open_file.readline().strip()
    return version

def read_aliases_file():  # todo - I think you know what I wanted to achieve, am was close!    list -> lines
    aliases_to_show = []
    with open('./resources/aliases.txt', 'r') as aliases_file:
        for line in aliases_file:
            if 'alias ' in line and '###' not in line:
                line = line.replace('alias ', '')
                aliases_to_show.append(line)

    with open('./.read_aliases.tmp', 'w') as write_obj:
        write_obj.write("".join(aliases_to_show))
    os.system('rm .read_aliases.tmp')  # cleanup after myself ;)

    return aliases_to_show

def load_config():
    if os.path.exists("./updater-config.json"):
        config = load_json("./updater-config.json")
    else:
        config = load_json('distr-updater-config.json')

    if config.debug_mode:
        config.user = config.debug_user
    else:
        config.user = config.pi_user

    if config.pi_4_cfg:
        config.pi_4_FLAG = True
    else:
        config.pi_4_FLAG = False

    if config.RH_version == 'master':
        config.server_version = 'master'
    if config.RH_version == 'beta':
        config.server_version = '2.1.0-beta.3'
    if config.RH_version == 'stable':
        config.server_version = '2.1.0'
    if config.RH_version == 'custom':
        config.server_version = 'X.X.X'  # paste custom version number here if you want to declare it manually

    if config.updates_without_pdf:
        config.update_mode = 'without pdf'
    else:
        config.update_mode = 'with pdf'
    return config


'''
This is a convenience method that uses lambda functions
to convert json data into accessible objects. 
Given file with:
{
    "name": "John Smith", 
    "hometown": {
        "name": "New York"
        , "id": 123
    }
}

running:
data = load_json(file_name) 

will let you do:
print(data.hometown.name)
>>> New York
'''


def load_json(file_name):
    data = {}
    if os.path.exists(file_name):
        with open(file_name) as open_file:
            data = json.loads(open_file.read(), object_hook=lambda d: Namespace(**d))
    return data


'''
quick wrapper around write json to normalize our parameters.
'''


def write_json(to_dump, file_name):
    with open(file_name, 'w') as open_file:
        if isinstance(to_dump, SimpleNamespace):
            json.dump(vars(to_dump), open_file, indent=4)
        else:
            json.dump(to_dump, open_file, indent=4)


'''
 wrapper around copy file to check if exists before copying
'''


def copy_file(src, tgt):
    if os.path.exists(src):
        copyfile(src, tgt)
