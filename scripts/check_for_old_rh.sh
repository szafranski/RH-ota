#!/bin/bash

cd ~/RH-ota || exit
ls ~ > old_rh.tmp
if grep -q 'RotorHazard_' old_rh.tmp; then
  echo > old_rh_found
else
  echo
fi
rm old_rh.tmp