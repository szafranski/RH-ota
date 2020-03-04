from smbus import SMBus

addr = 0x08 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

def main():
	selection=str(raw_input("What do you want to send?"))
	if selection=='1':
		bus.write_byte(addr, 0x1) # switch it on
	if selection=='2':
		bus.write_byte(addr, 0x0) # switch it on
	main()
main()

