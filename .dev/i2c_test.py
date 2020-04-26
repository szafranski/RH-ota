import os

detected_i2c_devices = os.popen("cat ./i2c_emulator").read()

# if '40 ' in detected_i2c_devices or '41 ' in detected_i2c_devices \
#         or '44 ' in detected_i2c_devices or '45 ' in detected_i2c_devices:
#     ina_found_flag = True


possible_rtc_addr = ['68 ', 'UU ', '50 ', '51 ', '52 ', '53 ', '54 ', '55 ', '56 ', '57 ']
for item in possible_rtc_addr:
    if item in detected_i2c_devices:
        rtc_found_flag = True
        break
else:
    rtc_found_flag = False

print(rtc_found_flag)
