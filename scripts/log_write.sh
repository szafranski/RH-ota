#!/bin/bash

cd /home/"${1}"/RH-ota || exit
mkdir log_data >/dev/null 2>&1
rm log_data/log.txt >/dev/null 2>&1
echo >./ log_data / log.txt
echo FILE /boot/config.txt | tee -a ./log_data/log.txt
echo -------------------------------- | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
cat /boot/config.txt | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo FILE /boot/cmdline.txt | tee -a ./log_data/log.txt
echo -------------------------------- | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
cat /boot/cmdline.txt | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo FILE updater-config.json | tee -a ./log_data/log.txt
echo -------------------------------- | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
cat ~/RH-ota/updater-config.json | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo FILE ~/.ota_markers/ota_config.txt | tee -a ./log_data/log.txt
echo -------------------------------- | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
cat ~/.ota_markers/ota_config.json | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo please wait few seconds
echo
echo pip3 packages | tee -a ./log_data/log.txt
echo -------------------------------- | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
pip3 freeze | tee -a ./log_data/log.txt
echo | tee -a ./log_data/log.txt
echo
echo LOGGING TO FILE - DONE
cd /home/"${1}"/RH-ota || exit
sleep 2
