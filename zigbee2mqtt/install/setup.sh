#!/bin/bash

#ls -l /dev/ttyACM0
#ls -l /dev/serial/by-id

sudo apt-get purge nodejs && sudo apt-get purge --auto-remove nodejs && sudo apt-get autoremove

# sudo apt-get install -y nodejs npm git make g++ gcc
# git clone https://github.com/Koenkk/zigbee2mqtt.git

sudo mv zigbee2mqtt /opt/zigbee2mqtt

cd install/

sudo cp config/configuration.yaml /opt/zigbee2mqtt/data/

sudo cp config/zigbee2mqtt.service /etc/systemd/system/

cd /opt/zigbee2mqtt
npm ci

# cd /opt/zigbee2mqtt
# npm start

sudo systemctl start zigbee2mqtt

sudo systemctl enable zigbee2mqtt.service

systemctl status zigbee2mqtt.service

# sudo systemctl stop zigbee2mqtt
# sudo systemctl start zigbee2mqtt
# sudo journalctl -u zigbee2mqtt.service -f