#!/bin/bash

sudo apt-get install git

source /var/opt/airva/apache2/install/setup.sh

source /var/opt/airva/mosquitto/install/setup.sh
 
source /var/opt/airva/poetry/setup.sh

source /var/opt/airva/nodeJS/install.sh

source /var/opt/airva/postgreSQL/install/setup.sh

source /var/opt/airva/thingsboard/install/setup.sh

source /var/opt/airva/zigbee2mqtt/install/setup.sh

source /var/opt/airva/WLAN/setup.sh

echo "Done :)"
