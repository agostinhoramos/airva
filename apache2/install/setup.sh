#!/bin/bash

# Config here
NAME="airva"
HOSTNAME=$NAME".local"
PORT=1333

sudo apt update
sudo apt purge -y apache2 
sudo apt install -y apache2
sudo ufw allow 'Apache'
sudo systemctl restart apache2
#sudo ufw status
#sudo systemctl status apache2

sudo a2enmod ssl
sudo a2enmod lbmethod_byrequests
sudo a2enmod rewrite
sudo a2enmod deflate
sudo a2enmod headers
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_wstunnel
sudo a2enmod proxy_ajp
sudo a2enmod proxy_connect
sudo a2enmod proxy_balancer
sudo a2enmod proxy_html

CPATH="/etc/apache2/sites-available/"
CONF_FILE=$CPATH"$NAME.conf"

cd $CPATH
sudo rm -rf $CONF_FILE
sudo chown $USER:$USER $CPATH

{
    echo "<VirtualHost *:80>"
    echo "   ServerName $HOSTNAME"
    echo "   ServerAlias $HOSTNAME"
    echo "   ServerAdmin webmaster@$HOSTNAME"
    echo "   RewriteEngine On"

    echo "   RewriteCond %{HTTP:Upgrade} =websocket [NC]"
    echo "   RewriteRule /(.*)            ws://127.0.0.1:$PORT/""$""1 [P,L]"
    echo "   RewriteCond %{HTTP:Upgrade} !=websocket [NC]"
    echo "   RewriteRule /(.*)            http://127.0.0.1:$PORT/""$""1 [P,L]"
    

    echo "   <Proxy balancer://backend-cluster>"
    echo "       BalancerMember http://127.0.0.1:$PORT/"
    echo "   </Proxy>"
    
    echo "   ProxyPass / balancer://backend-cluster/"
    echo "   ProxyPassReverse / balancer://backend-cluster/"
    echo "   ProxyRequests off"
    echo "</VirtualHost>"
} > $CONF_FILE

sudo a2dissite 000-default.conf
sudo a2ensite "$NAME.conf"
sudo systemctl restart apache2
#sudo systemctl status apache2
