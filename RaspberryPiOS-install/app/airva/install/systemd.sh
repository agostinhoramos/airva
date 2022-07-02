#!/bin/bash

service_name="airva";
myApp_name="main.py"

myApp_path="/var/opt/$service_name/RaspberryPiOS-install/app/airva/"
myApp_full_path="$myApp_path$myApp_name";
service_path="/etc/systemd/system/$service_name.service";
VIRTUAL_ENV="/home/master/.cache/pypoetry/virtualenvs/airva-*/bin/activate";

sudo chmod +x $myApp_full_path;
sudo rm -rf $service_path;

{
    echo "[Unit]"
    echo "Description=AirVA startup"
    echo ""
    echo "[Service]"
    echo "Type=idle"
    echo "Restart=on-failure"
    echo "User=master"
    echo "WorkingDirectory=$myApp_path"
    echo "ExecStart=/bin/sudo /bin/bash -c '. $VIRTUAL_ENV && python $myApp_name'"
    echo ""
    echo "[Install]"
    echo "WantedBy=multi-user.target"
} > $service_path;

sudo chmod 644 $myApp_full_path;
sudo systemctl daemon-reload;
sudo systemctl enable "$service_name.service";
sudo systemctl status "$service_name.service";

# sudo systemctl disable airva.service;
# sudo systemctl enable airva.service;
# sudo systemctl status airva.service;