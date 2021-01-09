#!/bin/bash

SERVICE_FILE=/lib/systemd/system/rotorhazard.service

old_python_service_statement="ExecStart=/usr/bin/python server.py"


if test -f "$SERVICE_FILE"; then

if grep -Fxq "$old_python_service_statement" "$SERVICE_FILE"; then
    echo "old python based RotorHazard autostart service found"
    sudo sed -i 's/python/python3/g' "$SERVICE_FILE"
    echo "changed to python3 based service"
else
    echo "RotorHazard autostart service is up to date"
fi
else
    echo "no RotorHazard autostart service found - no changes"
fi

printf "\n"

if grep -Fxq "python server.py" "/home/"$USER"/.bashrc"; then
    echo "old python based server-start alias found"
    sed -i 's/python server.py/python3 server.py/g' ~/.bashrc
    echo "changed to python3 based alias"
fi

