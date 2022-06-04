#!/bin/bash

sudo apt update && sudo apt upgrade -y

hostname="127.0.0.1"
username="mqttadmin"

mqtt_port=1883
mqtt_tls_port=8883
mqtt_websockets=8083

# CONFIG 0 or 1
enable_forwarding=1
enable_tls=1
enable_websockets=0

echo "Preparing to install MQTT..."
sudo rm /etc/mosquitto/conf.d/default.conf
sudo rm -rf "/etc/mosquitto/tmp/"
sudo rm /etc/mosquitto/ca_certificates/ca.crt
sudo rm /etc/mosquitto/ca_certificates/server.crt
sudo rm /etc/mosquitto/ca_certificates/server.key
sudo apt-get purge --remove mosquitto*
sleep 2

sudo apt install mosquitto -y
sudo systemctl status mosquitto
sudo systemctl restart mosquitto

echo "Please enter MQTT password of $username:";
sudo mosquitto_passwd -c /etc/mosquitto/passwd $username
sleep 1

sudo touch /etc/mosquitto/conf.d/default.conf
sudo chown $USER:$USER -R /etc/mosquitto/conf.d/default.conf
sudo echo -e "listener $mqtt_port localhost" >> /etc/mosquitto/conf.d/default.conf

if [ $enable_websockets -ge 1 ]; then
    sudo echo -e "\n# WEBSOCKETS" >> /etc/mosquitto/conf.d/default.conf
    sudo echo -e "listener $mqtt_websockets\nprotocol websockets\n" >> /etc/mosquitto/conf.d/default.conf
fi

if [ $enable_tls -ge 1 ]; then
    sudo mkdir "/etc/mosquitto/tmp/"
    cd /etc/mosquitto/tmp/

    echo "1 - First create a key pair for the CA"
    sudo openssl genrsa -des3 -out ca.key 2048
    echo "2 - Create a certificate for the CA using the CA key"
    sudo openssl req -new -x509 -days 1833 -key ca.key -out ca.crt
    echo "3 - Create a server key pair for Broker"
    sudo openssl genrsa -out server.key 2048
    echo "4 - Create a certificate request .csr"
    sudo openssl req -new -out server.csr -key server.key
    echo "5 - Using CA key to verify and sign the server certificate"
    sudo openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360
    
    echo "Moving to ca_certificates folder"
    sudo mv ca.crt /etc/mosquitto/ca_certificates/
    sudo mv server.crt /etc/mosquitto/ca_certificates/
    sudo mv server.key /etc/mosquitto/ca_certificates/
    sudo chmod 777 -R /etc/mosquitto/ca_certificates

    sudo echo -e "\n# TLS" >> /etc/mosquitto/conf.d/default.conf
    sudo echo -e "listener $mqtt_tls_port" >> /etc/mosquitto/conf.d/default.conf
    sudo echo -e "cafile /etc/mosquitto/ca_certificates/ca.crt\nkeyfile /etc/mosquitto/ca_certificates/server.key\ncertfile /etc/mosquitto/ca_certificates/server.crt\ntls_version tlsv1.2\n" >> /etc/mosquitto/conf.d/default.conf
fi
sudo echo -e "allow_anonymous true\npassword_file /etc/mosquitto/passwd" >> /etc/mosquitto/conf.d/default.conf

if [ $enable_forwarding -ge 1 ]; then
    sudo ufw allow $mqtt_port/tcp
    if [ $enable_tls -ge 1 ]; then
        sudo ufw allow $mqtt_tls_port/tcp
    fi
    if [ $enable_websockets -ge 1 ]; then
        sudo ufw allow $mqtt_websockets/tcp
    fi
fi

sudo systemctl restart mosquitto
sleep 2
echo "Done!"
