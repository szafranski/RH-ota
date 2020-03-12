

# Easy mange and update your RotorHazard installation. 

</br>
Additional features like nodes flashing are included.
</br></br>

If you want all hardware functionalities - visit: [Instructables page](https://www.instructables.com/id/RotorHazard-Updater/)
or check the [RotorHazard-Updater.pdf](/how_to/RotorHazard-Updater.pdf).

You may also read [update notes](update-notes.md) - new features are present.
</br></br>
#### Commands to download the repo onto Raspberry Pi (or Linux):
	cd ~
	sudo apt install zip unzip
	wget https://codeload.github.com/szafranski/RH-ota/zip/master -O tempota.zip
	unzip tempota.zip
	rm tempota.zip
	mv RH-ota-* RH-ota

#### Commands to open the software:
	sudo apt install python --> if needed
	
	cd ~/RH-ota
	python update.py

</br>

>This software is designed to run using python 2.7. Will be updated to be python 3 friendly, </br>
>when RotorHazard software will be converted as well.