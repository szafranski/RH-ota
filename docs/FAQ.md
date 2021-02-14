„Programmer not responding” shown during flashing attempt:

Means that you the Raspberry Pi cannot write information to an Arduinos via UART (Serial - RX and TX lines)

Possible causes:
1. Bad wiring - most common
2. Bad Raspberry Pi UART/Serial configuration - less common
3. Arduino contains code that makes UART line „busy” - possible
4. Arduino has incompatible bootloader burnt - not likely but possible

Fixes:
1. Check wiring 4 times. Most common mistakes are:
- RX and TX lines are swapped near the connectors (check R-Pi GPIO connector and Pi to PCB connection)
- bad voltage-divider resistors values (those 3 resistors near the right-bottom corner of the PCB) 
Horizontal one should read 10kOhms, vertical ones (which are „combined” - parallel connection) should read 5kOhm (half of a horizontal one value)

2. Manually set Serial protocol configuration by:
	1. Type „sudo raspi-config”
	2. Navigate to „Interfaces”
	3. Serial
	4. Enable Serial
	5. Disable Console output via serial (second question that you will be asked) - IMPORTANT!
	6. Exit rasps-config
	7. Reboot
	8. Try again

If you still get same error:
	1. Type „ls /dev | grep tty”
	2. You will see many „tty”-starting lines 
	3. Look for sth like „ttyS0”, „ttyS1” or „ttyAMA0” (Banana Pi uses „ttyS3” for example)
	4. One of above is the port name that you should use 
	5. Enter that port „name” during „First time flashing”
	6. Same port should be entered in a configuration wizard - after you confirm it works during „First time flashing”


3. Just flash all Arduinos with simple „blink sketch” using Arduino IDE using PC (or even a Raspberry Pi in ”Desktop mode”).
Remember to chose right Board (Arduino Nano), Processor (ATmega 328P old bootloader) and Port. 
Note: If the „Port” field is greyed out despite Arduino is connected - means that you have some drivers issues/no drivers at all.
Just google that and install drivers using „Devices Manager” for example. 
Perform „First time flashing” after that. If you stil get that error you can remove all nodes besides one (first) and than try. 
After successful flashing just place second node and so on. 


Additional info to points 2 and 3:

If you don’t want to perform „First time flashing” using Raspberry you can also flash Arduino-nodes using PC and Arduino IDE
and that just confirm that „automatic flashing” works. 

You could also perform „First time flashing” on the Pi with USB port selected - of course you will than just have to connect Arduinos 
one by one to given USB port of the Raspberry Pi (note: they have to be unplugged from the PCB before). That method only works 
when there are no other USB devices connected - assuming you wouldn’t manually select USB port other than USB0). 

Note: you can still got errors mentioned above when trying to perform „Automatic flashing” later so above are not a „fix”, 
you just skip one step that some people find as tricky. It is advised to perform „Automatic flashing” after initial setup 
and first „manual flashing” so you’d know that it will still work in a future.

4. Arduino in its infinite wisdom came up with an idea to make second iteration of Arduino Nano (with another bootloader).
It is not „better” it is just „different”. There is a small chance that you Arduinos contains that „newer” bootloader, that there is 
no bootloader at all or that the bootloader is just corrupted - cheap Chinese closes sometimes have that issue. You can check 
the bootloader version by trying to flash Arduino (using PC) with „newer booloader selected” in a Tools/Board menu.
If it can be successfully flashed with „newer booloader” selected - that may indicates that you have to burn normal/older boot loader.
If you want to do that you can use external programmer such as USB-ASP or just program one Arduino as a temporary programmer 
utilizing future named „Arduino as ISP” (NOT: ArduinoISP). To do that Google sth like „Flashing boot loader using Arduino as ISP”.
There are a lot of tutorials in that regard. 

