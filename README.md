![OTA Logo](./resources/ota_logo.png)

# Easy mange and update your [RotorHazard](https://github.com/RotorHazard/RotorHazard) installation. 



### Main features of the software:

1. Wizard install/update of RotorHazard server software
     - Choose which version of RotorHazard to install
     - Preserves existing RotorHazard config file.
     - Backup of existing RH install.
     - Automatically performs much of the RotorHazard specific Pi setup steps

1. Wizard install and update of RotorHazard nodes firmware.
     - Requires some hardware modification to enable - described [here](how_to/hw_mod_instructions.txt)

1. Automatic configuring Access Point
     - Hotspot: Configure always-on hotspot using Pi's built in Wifi 
        - You lose the ability to connect to the internet using built in Wifi. 
     - [Auto-Hotspot:](./AUTO_HOTSPOT.md) Automatically connect to known wifi if available, or become hotspot if no network is found. 
        - If your Pi has been configured to connect to WIFI, this option allows you to use that wifi when in range, and still create a hotspot when not in range.
        - full explanation: [here](https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/158-raspberry-pi-auto-wifi-hotspot-switch-direct-connection)

Helpful developer/back-end options:
1. Installing AVRdude
1. Adding aliases to the system
1. Script for installing dependencies 
1. Showing Raspberry GPIO in the terminal
1. Embedded logging feature with an option to upload log file to the cloud 
<br/>

If you use old, Delta5 boards but you still want all hardware functionalities - visit: [Instructables page](https://www.instructables.com/id/RotorHazard-Updater/) - to get some context
or check the file with [hardware mod instructions](/how_to/hw_mod_instructions.txt).

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
#### Commands to download the software onto Raspberry Pi (or Linux):
**Note:**  This software will automatically install all necessary dependencies

    cd ~
    wget https://codeload.github.com/szafranski/RH-ota/zip/main_stable -O tempota.zip
    unzip tempota.zip
    rm tempota.zip
    mv RH-ota-* RH-ota
    chmod +x ~/RH-ota/ota.sh
    
    *Change 2nd line with what's below if you want to install the beta version: 
    
    wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip

#### Commands to open the software:
    
    cd ~/RH-ota
    ./ota.sh

<br/>
We assume in our instructions and provided setup process that you already have your Raspbian OS set up. 
If not, please follow those instructions: [Raspbian setup instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).
<br/>
<br/>

### ~~ *Toss a coin to a Witcher* section ~~

<br/>
I started this project as a way to help the community. I also found it very interesting and meaningful to explore new territories and do the best I can so end user can be satisfied to as high degree as possible. We spent long hours on testing, coding and troubleshooting. If you feel that this work was valuable and you want to say "thank you" that way, you can use
 
 [PayPal donation link](https://www.paypal.com/donate/?token=9BLz3dIwcuO_YUjh43IHLai6ZgaOD9BpDkmSfdN_1_EDeJmSEeIqnWDqdiPs27nH9SFAiW&country.x=PL&locale.x=PL). Every amount is meaningful. Remember that our help and contribution is NOT conditional :)
<br/> 
<br/>

>If you want detailed description of this software and actions that are being performed during operations</br>
>or you have some programming experience you may read [developer notes](/docs/dev-notes.txt). Legal stuff - here: [license file](/docs/LICENSE.txt).
