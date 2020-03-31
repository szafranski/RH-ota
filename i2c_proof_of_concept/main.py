from flash_common import flash
from time import sleep

addr1 = 0x08
addr2 = 0xa
addr3 = 0xa
addr4 = 0xa

addr_list = [addr1, addr2, addr3, addr4]

for addr in addr_list:
    flash(addr)
    sleep(2)
