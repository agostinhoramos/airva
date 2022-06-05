#!/bin/bash

sudo apt update && sudo apt upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo groupadd docker

sudo usermod -aG docker $USER

newgrp docker 

docker version

# docker run hello-world
# sudo apt-get purge docker-ce
# sudo rm -rf /var/lib/docker

# https://docs.docker.com/engine/install/linux-postinstall/