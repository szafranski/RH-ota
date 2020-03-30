#!/bin/bash

cd /home/"${1}"/RH-ota || exit
echo
echo Please wait, file is being uploaded...
echo
rm ./log_data/log_name.txt >/dev/null 2>&1
rm ./log_data/log_code.txt >/dev/null 2>&1
echo "${2}" >./log_data/log_name.txt
curl --upload-file ./log_data/log.txt https://transfer.sh/"${2}"_log.txt | tee -a ./log_data/log_code.txt
echo
sed -i 's/https:\/\/transfer.sh\///g' ./log_data/log_code.txt
sed -i 's/\/${1}_log.txt//g' ./log_data/log_code.txt
echo
echo ------------------------------
echo
echo Tell your favourite developer those:
echo
echo User name: ${2}
cd /home/"${1}"/RH-ota || exit
