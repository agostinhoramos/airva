#!/bin/bash

sudo apt install ufw -y
sudo ufw allow 1883/tcp

FPATH="/var/opt/airva/WLAN/"
sudo $FPATH"/wl.sh" "CASA RAMOS" "ngueTela" "WPA-PSK" "PT" "wlan0"
sleep 5
sudo $FPATH"/ap.sh" "DIRECT-AIRVA" "ABCDEFGH4321" 1 "192.168.153.1" "wlan1" "PT"