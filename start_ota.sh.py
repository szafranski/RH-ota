import sys


def main():
    old_python_error_message = """

Program detected that you are using python version 3.5 or lower.
This software requires python 3.6 or higher. You can manually update apt sources
for your OS - that process is described with details in the file
'~/RH-ota/docs/python36help.txt' - check here or on the GitHub repo page.

You could also just burn SD-Card with Raspbian Buster (10) or newer since those
support python 3.6+ natively. Using newer OS is advised anyways.

If you want to check currently used Raspbian OS version - type: 'cat /etc/os-release'
If you want to check currently used python3 version - type: 'python3 --version'
If you want to list all python versions on your OS right now - type: 'python' and hit Tab twice
"""
    if (sys.version_info.major == 3) and (sys.version_info.minor < 6):
        print("This program requires python3.6 or newer")
        print(old_python_error_message)
    else:
        print("Program starts...")
        import update
        update.main()


if __name__ == "__main__":
    main()
