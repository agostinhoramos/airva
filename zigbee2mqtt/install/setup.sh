#!/bin/bash

#ls -l /dev/ttyACM0
#ls -l /dev/serial/by-id

sudo apt-get purge nodejs && sudo apt-get purge --auto-remove nodejs && sudo apt-get autoremove

sudo apt-get install -y nodejs npm git make g++ gcc
