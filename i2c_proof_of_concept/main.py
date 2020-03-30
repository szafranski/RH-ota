from common import flash
from time import sleep


addr_list = [0x08, 0x0a]

for addr in addr_list:
    flash(addr)
    sleep(2)

