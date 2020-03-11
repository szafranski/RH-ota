# use arrows, pg up and pg down or space bar to navigate
# hit 'q' to exit now


		UPDATE NOTES:
		^^^^^^^^^^^^

2.2.9e

Added functions and modules
Beter configuration handling
Faster internet checker

2.2.9c

Server start links as a sh scipts - simpler, 
allows stopping server and coming back to ota program


2.2.9a

Checking internet connection before performing server update
or installation - prevents errors and config loss

______________________________________________________________

2.2.8n

Checking internet connection before performing self-update
to prevent deleting RH-ota folder when no new version available
Done in bash - waiting for python3 support

2.2.8k

Much smaller updates sizes - another way of handloing downloads
No config file after server starts - fixed

2.2.8h

Added:
option to disable downloading PDF file with every update
updater-config.json
change the line to: 
	"updates_without_pdf" : 1

2.2.8e

Added:
access point automatic configuration
detailed explanation in Access Point menu
features compatibility with previous installations
new aliases (uu, otacfg, otacpcfg, home) - auto added

Polished and much more reliable:
self-updater
general code look
no error messages if no folders were found
runs ok on Windows - just for a preview 

Improved:
descriptions in the software

Visual improvements:
menus and descriptions

______________________________________________________________

2.2.5 and higher

If you performed an update from 2.2.4 version or previous 
and you want to use custom pins as reset pins:

Change line in updater-config.json file so it looks like:

	"pins_assignment" : "custom"

So the file looks like this:

{
	"pi_user" : (...),
	"RH_version" : (...),
	"debug_user" : (...),
	"country" : (...),
	"nodes_number" : (...),
	"debug_mode" : 0,
	"pins_assignment" : "custom"
}

And than edit lines 60 to 67 in nodes_update.py file.

nano nodes_update.py

Happy flyin'!
______________________________________________________________

# EXIT by hitting "q" 
