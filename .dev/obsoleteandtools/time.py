from time import sleep
import time


before_millis = int(round(time.time() * 1000))
print before_millis

print before_millis
sleep(2)
now_millis = int(round(time.time() * 1000))

print now_millis

sleep(2)

millis_gone = now_millis - before_millis

print millis_gone
