FROM ubuntu:20.04

LABEL release-date="2022-03-12" maintainer="Agostinho Ramos <agostinhopina095@gmail.com>"

RUN apt update && apt install openssh-server sudo -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 user 

RUN  echo 'user:1234' | chpasswd

RUN service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]