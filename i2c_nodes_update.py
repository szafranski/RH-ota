import smbus 

# Slave Addresses for Arduinos 
ARDUINO_1_ADDRESS = 8 # I2C Address of Arduino 1 
ARDUINO_2_ADDRESS = 10 # I2C Address of Arduino 2 
ARDUINO_3_ADDRESS = 12 # I2C Address of Arduino 3 
ARDUINO_4_ADDRESS = 14 # I2C Address of Arduino 4 
ARDUINO_5_ADDRESS = 16 # I2C Address of Arduino 5 
ARDUINO_6_ADDRESS = 18 # I2C Address of Arduino 6 
ARDUINO_7_ADDRESS = 20 # I2C Address of Arduino 7 
ARDUINO_8_ADDRESS = 22 # I2C Address of Arduino 8 

# Create the I2C bus 
I2Cbus = smbus.SMBus(1) 

aSelect = raw_input("Which Arduino (1-8): ") 
bSelect = raw_input("On or Off (on/off): ") 

if aSelect == 1: 
	SlaveAddress = ARDUINO_1_ADDRESS 
elif aSelect == 2: 
	SlaveAddress = ARDUINO_2_ADDRESS 
elif aSelect == 3: 
	SlaveAddress = ARDUINO_3_ADDRESS 
elif aSelect == 4: 
	SlaveAddress = ARDUINO_4_ADDRESS 
elif aSelect == 5: 
	SlaveAddress = ARDUINO_5_ADDRESS 
elif aSelect == 6: 
	SlaveAddress = ARDUINO_6_ADDRESS 
elif aSelect == 7: 
	SlaveAddress = ARDUINO_7_ADDRESS 
elif aSelect == 8: 
	SlaveAddress = ARDUINO_8_ADDRESS 
else: 
	quit() 

if bSelect != "on" or bSelect != "off": quit() 

BytesToSend = ConvertStringsToBytes(bSelect) 
I2Cbus.write_i2c_block_data(SlaveAddress, 0x00, BytesToSend) 
print("Sent " + SlaveAddress + " the " + bSelect + " command.") 

# This function converts a string to an array of bytes. 
def ConvertStringToBytes(src): 
	converted = [] 
	for b in src: 
		converted.append(ord(b)) 
	return converted</pre>