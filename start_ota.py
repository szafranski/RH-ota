import sys


def main():
    old_python_error_message = """

The program detected that you are using python version 3.5 or lower.
This software requires python 3.6 or higher. You can manually update apt sources
for your OS - that process is described with details in the file
'~/RH-ota/docs/python36help.txt' - check here or on the GitHub repo page.

You could also just burn SD-Card with Raspbian Buster (10) or newer since those
support python 3.6+ natively. Using newer OS is advised anyways.

To check currently used Raspbian OS version - type: 'cat /etc/os-release'
To check currently used python3 version - type: 'python3 --version'
To list all python versions installed on your OS - type: 'python' and hit Tab twice

Detailed instructions what to do now can be found in: RH-ota/docs/python36_help.txt

"""
    if sys.version_info < (3, 6):
        print(2 * "\n" + 80 * "-" + "\n" + 80 * "-")
        print("\n\nThis program requires python3.6 or newer")
        print(old_python_error_message)
    else:
        print("Program starts...")
        import update
        update.main()


if __name__ == "__main__":
    main()
