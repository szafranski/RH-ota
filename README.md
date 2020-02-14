# RH_node_ota_updates
plans and instructions

Concerns. Knows issues

Uploading with bootloader? What if no? 

Rescue button/instructions/jumper?

How channel sellecting works? Is it affected? Solution - diodes? software spi?

Bad fuses? Anyone?

Only ground pin nodes or both versions?

What about new pcb design?

3. Consider using separating diodes - rx5808

4. Consider using logic level converter - rather not, voltage divider on MISOline?


State of the project for now:

Arduino programmed by Rpi pins - DONE

Multiple Arduinos programmed at once - DONE

Ability to program Arduinos one after another - DONE

Confirmed consistency - DONE

RSSI readouts - WORKS after flashing

Tutorial how to do this - DONE

Things to consider:
1. Why two of Arduinos during tests got bad fuses after using avrdude - BIG ISSUE
2. Is there a way to program Arduino one by one, not all at once - DONE!
3. Consider using separating diodes - rx5808
4. Consider using logic level converter - rather not
