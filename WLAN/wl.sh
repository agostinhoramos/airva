#!/bin/bash

# WLAN Receiver

wlanSSID="$1"
wlanPASS="$2"
KEY_MGMT="$3"
COUNTRY="$4"
WLAN="$5"

ws_wlan="/etc/wpa_supplicant/wpa_supplicant-$WLAN.conf"
wlan_network="/etc/systemd/network/12-$WLAN.network"

output=$(/sbin/iw dev)
if [[ $output =~ $WLAN ]]; then

    if [[ ! -f "/etc/network/interfaces" ]]; then
        sudo systemctl mask networking.service dhcpcd.service
        mv /etc/network/{interfaces,interfaces~} # Backup file
        cp /etc/{resolv.conf,resolv.conf~}
        sed -i '1i resolvconf=NO' /etc/resolvconf.conf
        sudo systemctl enable systemd-networkd.service systemd-resolved.service
        ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
    fi

    {
        echo "country=$COUNTRY"
        echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"
        echo "update_config=1"
        echo "network={"
        echo '  ssid="'$wlanSSID'"'
        echo '  psk="'$wlanPASS'"'
        echo '  key_mgmt='$KEY_MGMT''
        echo "}"
    } > $ws_wlan

    {
        echo "[Match]"
        echo "Name=$WLAN"
        echo "[Network]"
        echo "DHCP=yes"
    } > $wlan_network

    sudo chmod 600 $ws_wlan
    sudo systemctl disable wpa_supplicant.service
    sudo systemctl enable wpa_supplicant@wlan1.service

    sudo systemctl restart systemd-networkd.service
    sudo systemctl restart wpa_supplicant@$WLAN.service

    echo "1"
else
    echo "0"
fi