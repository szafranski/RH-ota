# „Programmer not responding” shown during flashing attempt:

Means that you the Raspberry Pi cannot write information to an Arduinos via UART (Serial - RX and TX lines)

## Possible causes:
1. Bad wiring - most common
1. Bad Raspberry Pi UART/Serial configuration - less common
1. Arduino contains code that makes UART line „busy” - possible
1. Arduino has an incompatible bootloader burnt - not likely but possible
1. One (or more) Arduino is just broken hardware-wise - not impossible

## Fixes for each cause:

### 1. Check wiring 4 times. Most common mistakes are:
- RX and TX lines are swapped near the connectors (check Pi's GPIO connector and Pi to PCB connection)
- bad voltage-divider resistors values (those 3 resistors near the right-bottom corner of the PCB) 
Horizontal one should read about 10kOhms, vertical ones (which are „combined” - parallel connection) should read 5kOhm (half of a horizontal one value)
- solder "blobs" are shorting RX or TX line with some other lines or with each other

### 2. Manually set Serial protocol configuration by:
	1. Type „sudo raspi-config”
	2. Navigate to „Interfaces”
	3. Serial
	4. Enable Serial
	5. Disable Console output via serial (second question that you will be asked) - IMPORTANT!
	6. Exit rasps-config
	7. Reboot
	8. Try again

#### If you still get same error:
	1. Type „ls /dev | grep tty”
	2. You will see many „tty”-starting lines 
	3. Look for sth like „ttyS0”, „ttyS1” or „ttyAMA0” (Banana Pi uses „ttyS3” for example)
	4. One of above is the port name that you should use 
	5. Enter that port „name” during „First time flashing”
	6. Same port should be entered in a configuration wizard - after you confirm it works during „First time flashing”


### 3. Just flash all Arduinos with simple „blink sketch” using Arduino IDE using PC (or even a Raspberry Pi in ”Desktop mode”).
Remember to chose right Board (Arduino Nano), Processor (ATmega 328P old bootloader) and Port. 
Note: If the „Port” field is greyed out despite Arduino is connected - means that you have some drivers issues/no drivers at all.
Just google that and install drivers using „Devices Manager” for example. 
Perform „First time flashing” after that. If you stil get that error you can remove all nodes besides one (firstly try in "slot 1", in case of error try another one) and then try. 
After successful flashing just place second node in another slot and so on. 

<br>

#### Additional info to points 2 and 3:

If you don’t want to perform „First time flashing” using Raspberry you can also flash Arduino-nodes using PC and Arduino IDE
and that just confirm that „automatic flashing” works. 

You could also perform „First time flashing” on the Pi with USB port selected - of course you will than just have to connect Arduinos 
one by one to given USB port of the Raspberry Pi (note: they have to be unplugged from the PCB before). That method only works 
when there are no other USB devices connected - assuming you wouldn’t manually select USB port other than USB0). 

<b>Note:</b> you can still got errors mentioned above when trying to perform „Automatic flashing” later so above are not a „fixes”, 
you just skip one step that some people find as tricky. It is advised to perform „Automatic flashing” after initial setup 
and first „manual flashing” so you’d know that it will still work in a future.

### 4. Arduino in its infinite wisdom came up with an idea to make second iteration of Arduino Nano (with another bootloader) and cheap clones are not helping
It is not „better” - it is just different. There is a small chance that your Arduinos contains that „newer” bootloader, that there is 
no bootloader at all or that the bootloader is just corrupted - cheap Chinese closes sometimes have that issue. You can check 
the bootloader version by trying to flash Arduino (using PC) with „newer booloader" selected in a Tools/Board menu.
If it can be successfully flashed with „newer booloader” selected - that may indicates that you have to burn normal/older bootloader.
If you want to do that, you can use external programmer such as USB-ASP or just program one Arduino as a temporary programmer 
utilizing feature named „Arduino as ISP” (NOT: "ArduinoISP"). To performing that just Google sth like „Burning bootloader using Arduino as ISP”.
There are a lot of tutorials in that regard.

If you have Arduinos from few different batches (they are often different color-wise etc) try to remove variables. Use those from same batch, check. Use those from different one, check.

### 5. Everything can just "be broken"
Assume that one Arduino is broken and try with other ones. Remove one and check etc.

### * You can handle that :) * 
Remember - when everyting is configured properly hardware and software -wise it just HAVE TO work. Don't be frustrated, check 3 times, have fun. It works :)