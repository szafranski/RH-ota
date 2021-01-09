#!/bin/bash

FILE=/lib/systemd/system/rotorhazard.service

old_python_statement="ExecStart=/usr/bin/python server.py"


if test -f "$FILE"; then

if grep -Fxq "$old_python_statement" "$FILE"; then
    echo "old python based RotorHazard autostart service found"
    sed -i 's/python/python3/g' "$FILE"
    echo "changed to python3 based service"
else
    echo "no obsolete RotorHazard autostart service found"
fi
else
    echo "no RotorHazard autostart service found - no changes"
fi
