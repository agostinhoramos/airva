#!/bin/bash

PATH="/var/opt/airva/RaspberryPiOS-install/app/airva";
cd $PATH;
iPATH=$PATH"/install/";
/bin/sudo chmod +x $iPATH"systemd.sh";
/bin/sudo $iPATH"systemd.sh";