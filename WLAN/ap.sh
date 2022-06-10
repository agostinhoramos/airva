#!/bin/bash

# ACCESS POINT

NEW_SSID="$1"
NEW_PASS="$2"
SECURITY_LEVEL="$3"
NETWORK="$4"
WLAN="$5"
COUNTRY="$6"

KEY_MGMT=""
PROTO=""
PAIRWISE=""

if [ $SECURITY_LEVEL -eq "1" ]; then
    KEY_MGMT="WPA-PSK"
    PROTO="WPA2"
    PAIRWISE="CCMP"
elif [ $SECURITY_LEVEL -eq "2" ]; then
    KEY_MGMT="WPA-EAP"
    PROTO="WPA2"
    PAIRWISE="CCMP TKIP"
fi

wpconf="/etc/wpa_supplicant/wpa_supplicant-$WLAN.conf"
wlan_network="/etc/systemd/network/08-$WLAN.network"

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
        echo "ctrl_interface=/var/run/wpa_supplicant"
        echo "ctrl_interface_group=0"
        echo "update_config=1"
        echo "network={"
        echo '  ssid="'${NEW_SSID}'"'
        if [ -z "$NEW_PASS" ]; then
            echo "  key_mgmt=NONE"
        else
            echo '  psk="'${NEW_PASS}'"'
            echo "  key_mgmt=$KEY_MGMT"
            if [ ! -z "$PROTO" ]; then
                echo "  proto=$PROTO"
            fi
            if [ ! -z "$PAIRWISE" ]; then
                echo "  pairwise=$PAIRWISE"
                echo "  group=$PAIRWISE"
            fi
        fi
        echo "  priority=5"
        echo "  scan_ssid=1"
        echo "  mode=2"
        echo "  frequency=2412"
        echo "}"
    } > $wpconf

    sudo chmod 600 $wpconf

    sudo systemctl disable wpa_supplicant.service
    sudo systemctl enable wpa_supplicant@$WLAN.service

    {
        echo "[Match]"
        echo "Name=$WLAN"
        echo "[Network]"
        echo "Address=$NETWORK/24"
        echo "IPMasquerade=yes"
        echo "IPForward=yes"
        echo "DHCPServer=yes"
        echo "[DHCPServer]"
        echo "DNS=8.8.8.8"
    } > $wlan_network

    sudo systemctl restart systemd-networkd.service
    sudo systemctl restart wpa_supplicant@$WLAN.service

    echo "1"
else
    echo "0"
fi