The auto-hotspot feature as implemented
by  https://www.raspberryconnect.com/projects/65-raspberrypi-hotspot-accesspoints/158-raspberry-pi-auto-wifi-hotspot-switch-direct-connection
Is a handy feature to have if you use the timer at home and away. When you are at home, the timer can connect
to your home Wi-Fi, so you can access it from any computer (or smart device) on your network.  
When you are away from home the timer will automatically set up a hotspot that you can connect to for race management.
The built-in Wi-Fi hotspot does not have great range, so this feature is only useful if the timer
is close to the computer that is managing it.  
It also helps to have the timer off the ground to improve range, and do not shield the pi with metal tape.
If you are going to shield your nodes to improve accuracy, it would be good to have the pie outside that shielding.

* When connected to Wi-Fi, most routers will allow you to use bonjour to connect to the Raspberry Pi
  So you can ssh to your RotorHazard device by doing: `ssh pi@rasberrypi.local`
* If you change the hostname: ether through GUI or via `raspi-config` > `networking` > `hostname` to something like:
  **rotorhazard**  then your timer would be assessable as `ssh pi@rotorhazard.local`

* When the timer is not within range of a known Wi-Fi network, it will set up a hotspot for you.
  Connect to the hotspot and go to `10.0.0.5` to access the timer. eg: `ssh pi@10.0.0.5` 
 

