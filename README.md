![OTA Logo](./resources/ota_logo.png)

# Easy mange and update your [RotorHazard](https://github.com/RotorHazard/RotorHazard) installation. 



### Main features of the software:

1. Wizard install/update of RotorHazard server software
     - Choose which version of RotorHazard to install
     - Preserves existing rotorhazard config file.
     - Backup of existing RH install.
     - Automatically performs much of the RotorHazard specific Pi setup steps

1. Wizard install of RotorHazard nodes firmware.
     - Requires some hardware modification to enable

1. Automatic configuring Access Point
     - Hotspot: Configure always-on hotspot using Pi's built in Wifi 
     - Auto-Hotspot: Automatically connect to known wifi if available, or become hotspot if no network is found. 
        - explanation: https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/158-raspberry-pi-auto-wifi-hotspot-switch-direct-connection

Helpful developer/back-end options:
1. Installing avrdude
1. Adding aliases to the system
1. Script for installing dependencies 
1. Showing Raspberry GPIO in the terminal
1. Embedded logging feature with an option to upload log file to the cloud 
<br/>

If you want all hardware functionality - visit: [Instructables page](https://www.instructables.com/id/RotorHazard-Updater/)
or check the [RotorHazard-Updater.pdf](/how_to/RotorHazard-Updater.pdf).

You may also read [update notes](/docs/update-notes.txt) - new features are present.
</br></br>
##
### Credits:
[szafranski](https://github.com/szafranski) - project idea, first implementations, flashing part, initial coding
</br>

[Dave](https://github.com/just-david) - ongoing contribution, BIG coding help, debugging, smart hot-spot
</br>

[Michael FPV](https://github.com/HazardCreative) - consulting and RotorHazard compatibility issues
</br>

[Facebook Group](https://www.facebook.com/groups/207159263704015) members as well as  software and hardware testers
</br>
##
#### Commands to download the repo onto Raspberry Pi (or Linux):
    cd ~
    sudo apt install zip unzip
    wget https://codeload.github.com/szafranski/RH-ota/zip/main_stable -O tempota.zip
    unzip tempota.zip
    rm tempota.zip
    mv RH-ota-* RH-ota

#### Commands to open the software:
    
    cd ~/RH-ota
    sh ./ota.sh

<br/>

>If you want detailed description of this software and actions that are being performed during operations</br>
>or you have some programming experience you may read [developer notes](/docs/dev-notes.txt). Legal stuff - here: [license file](/docs/LICENSE.txt).
