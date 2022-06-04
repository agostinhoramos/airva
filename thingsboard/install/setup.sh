#!/bin/bash

# Get ready to install
sudo apt update && sudo apt upgrade -y
sudo rm -rf /tmp/*
cd /tmp/

sudo apt install openjdk-11-jdk

sudo wget https://github.com/thingsboard/thingsboard/releases/download/v3.3.4.1/thingsboard-3.3.4.1.deb

sudo dpkg -i thingsboard-3.3.4.1.deb