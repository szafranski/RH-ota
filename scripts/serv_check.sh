#!/bin/bash

FILE=/lib/systemd/system/rotorhazard.service

old_python_statement="ExecStart=/usr/bin/python server.py"


if test -f "$FILE"; then

if grep -Fxq "$old_python_statement" "$FILE"; then
    echo "old python based RotorHazard autostart service found"
    sed -i 's/python/python3/g' "$FILE"
    echo "changed to python3 based service"
else
    echo "RotorHazard autostart service is up to date"
fi
else
    echo "no RotorHazard autostart service found - no changes"
fi

# below ensures that if user had "server start" alias added it will be updated as well
sed -i 's/python server.py/python3 server.py/g' ~/.bashrc
