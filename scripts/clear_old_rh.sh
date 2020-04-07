#!/bin/bash

#if [ -d "/home/${1}/RotorHazard_*" ]; then
  cp -r ~/RotorHazard ~/temp_RotorHazard
  rm -rf ~/RotorHazard_*
  mv ~/temp_RotorHazard ~/RotorHazard
  echo old installation directories cleaned
#else
#  echo no old installation directories found
#fi
# todo change to python's Path etc