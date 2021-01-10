import os

detected_i2c_devices = os.popen("cat ./i2c_emulator").read()

# if '40 ' in detected_i2c_devices or '41 ' in detected_i2c_devices \
#         or '44 ' in detected_i2c_devices or '45 ' in detected_i2c_devices:
#     ina_found_flag = True

rtc_found_flag = False
possible_rtc_addr = ['68 ', 'UU ', '50 ', '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ']
for item in possible_rtc_addr: rtc_found_flag = True if item in detected_i2c_devices else rtc_found_flag

print(rtc_found_flag)
