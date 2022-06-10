#!/bin/bash

sudo apt update && sudo apt upgrade -y

hostname="127.0.0.1"
username="mqttadmin"
password="over224433"

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
sudo apt-get purge --remove mosquitto* -y

sleep 2

sudo apt install mosquitto -y
# sudo systemctl status mosquitto
sudo systemctl restart mosquitto

echo -e "$password\n$password\n" | sudo mosquitto_passwd -c /etc/mosquitto/passwd $username
sleep 1

sudo touch /etc/mosquitto/conf.d/default.conf
sudo chown $USER:$USER -R /etc/mosquitto/conf.d/default.conf
sudo echo -e "listener $mqtt_port 0.0.0.0" >> /etc/mosquitto/conf.d/default.conf

if [ $enable_websockets -ge 1 ]; then
    sudo echo -e "\n# WEBSOCKETS" >> /etc/mosquitto/conf.d/default.conf
    sudo echo -e "listener $mqtt_websockets 0.0.0.0\nprotocol websockets\n" >> /etc/mosquitto/conf.d/default.conf
fi

if [ $enable_tls -ge 1 ]; then
    sudo mkdir "/etc/mosquitto/tmp/"
    cd /etc/mosquitto/tmp/

    COUNTRY="PT"
    STATE="Lisbon"
    LOCALITY="Lisbon"
    ORG_NAME="IPG"
    ORG_U_NAME="IPG"
    DOMAIN="airva.local"
    PASSWORD="over1234"

    SUBJECT="/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORG_NAME/OU=$ORG_U_NAME/CN=$DOMAIN"

    # 1 - First create a key pair for the CA
    sudo openssl genrsa -des3 -passout pass:$PASSWORD -out ca.key 2048

    # 2 - Create a certificate for the CA using the CA key
    sudo openssl req -passin pass:$PASSWORD -new -x509 -days 1833 -key ca.key -out ca.crt -subj "$SUBJECT"

    # 3 - Create a server key pair for Broker
    sudo openssl genrsa -out server.key 2048

    # 4 - Create a certificate request .csr
    sudo openssl req -new -key server.key -out server.csr -subj "$SUBJECT"

    # 5 - Using CA key to verify and sign the server certificate
    sudo openssl x509 -req -passin pass:$PASSWORD -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360
    
    echo "Moving to ca_certificates folder"
    sudo mv ca.crt /etc/mosquitto/ca_certificates/
    sudo mv server.crt /etc/mosquitto/ca_certificates/
    sudo mv server.key /etc/mosquitto/ca_certificates/
    sudo chmod 777 -R /etc/mosquitto/ca_certificates
    {
        echo ""
        echo "# TLS"
        echo "listener $mqtt_tls_port 0.0.0.0"
        echo "cafile /etc/mosquitto/ca_certificates/ca.crt"
        echo "keyfile /etc/mosquitto/ca_certificates/server.key"
        echo "certfile /etc/mosquitto/ca_certificates/server.crt"
        echo "tls_version tlsv1.2"
    } >> /etc/mosquitto/conf.d/default.conf
fi

{
    echo ""
    echo "allow_anonymous true"
    echo "password_file /etc/mosquitto/passwd"
} >> /etc/mosquitto/conf.d/default.conf

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
