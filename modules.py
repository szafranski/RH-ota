from configparser import ConfigParser
from shutil import copyfile
from time import sleep
import os
import platform
import sys
import json
import time
from types import SimpleNamespace as Namespace


#  todo add an RH version to modules so it can be read by other files like i2c nodes_update


def clear_the_screen():
    sleep(0.05)
    if platform.system() == "Windows":
        os.system("cls")
    if platform.system() == "Linux":
        os.system("clear")
    else:
        print(("\n" * 200))
    sleep(0.05)


def dots2sec():
    for i in range(30):
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(0.0666)
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
    logo = '''
    \n    
    #######################################################################
    ###                                                                 ###
    ###           {orange}{bold} RotorHazard {endc}                     ###
    ###                                                                 ###
    ###                {bold}OTA Updater and Manager{endc}              ###
    ###                                                                 ###
    #######################################################################
    {endc}
    '''.format(bold=Bcolors.BOLD_S, underline=Bcolors.UNDERLINE_S, endc=Bcolors.ENDC_S,
               blue=Bcolors.BLUE_S, yellow=Bcolors.YELLOW_S, red=Bcolors.RED_S, orange=Bcolors.ORANGE_S)

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


def internet_check(user):
    print("\nPlease wait - checking internet connection state...\n")
    before_millis = int(round(time.time() * 1000))
    os.system(". /home/" + user + "/RH-ota/open_scripts.sh; net_check")
    while True:
        now_millis = int(round(time.time() * 1000))
        time_passed = (now_millis - before_millis)
        if os.path.exists("./index.html"):
            internet_flag = 1
            break
        elif time_passed > 10100:
            internet_flag = 0
            break
    os.system("rm /home/" + user + "/RH-ota/index.html > /dev/null 2>&1")
    os.system("rm /home/" + user + "/RH-ota/wget-log* > /dev/null 2>&1")
    os.system("rm /home/" + user + "/index.html > /dev/null 2>&1")
    os.system("rm /home/" + user + "/wget-log* > /dev/null 2>&1")

    return internet_flag


def parser_write(parser, config):
    user = config.user
    try:
        with open(f'/home/{user}/.ota_markers/ota_config.txt', 'w') as configfile:
            parser.write(configfile)
    except IOError as _:  # in python _ means ignore this variable.
        print("Config file does not exist and could not be created.")


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

    parser = ConfigParser()
    parser.read('/home/' + config.user + '/.ota_markers/ota_config.txt')

    return parser, config


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
 wrapper around copy file to check if exists before copying
'''


def copy_file(src, tgt):
    if os.path.exists(src):
        copyfile(src, tgt)
