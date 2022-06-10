#!/bin/bash

PSQL_PSSW="over_332244"

sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password '$PSQL_PSSW';"

sudo -u postgres psql -U postgres -d postgres -c "CREATE DATABASE thingsboard;";

# Get ready to install
sudo apt update && sudo apt upgrade -y
sudo rm -rf /tmp/*
cd /tmp/

sudo apt install -y openjdk-11-jdk

sudo wget https://github.com/thingsboard/thingsboard/releases/download/v3.3.4.1/thingsboard-3.3.4.1.deb

sudo dpkg -i thingsboard-3.3.4.1.deb

sudo cp -f /var/opt/airva/thingsboard/install/thingsboard.conf /etc/thingsboard/conf/

sudo cp -f /var/opt/airva/thingsboard/install/thingsboard.yml /usr/share/thingsboard/conf/

sudo /usr/share/thingsboard/bin/install/install.sh --loadDemo

sleep 2

sudo service thingsboard start