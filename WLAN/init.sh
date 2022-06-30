#!/bin/bash

# CONFIGURATIONS TO BE CHANGED ####
WLAN0="wlan0"
WLAN1="wlan1"
NETWORK="133"
COUNTRY="PT"

ORIGINAL_SSID="dragino-1bc528"
ORIGINAL_PASS="dragino+dragino"
NEW_SSID="DIRECT-AIRVA"
NEW_PASS="ABCDEFGH4321"

## ALL FUNCTIONS
show_configurations() {
    echo "Current configurations: "
    echo "WLAN0: $WLAN0"
    echo "WLAN1: $WLAN1"
    echo "NEW_SSID: $NEW_SSID"
    echo "NEW_PASS: $NEW_PASS"
    echo "NETWORK: $NETWORK"
    echo "COUNTRY: $COUNTRY"
    sleep 1
}
check_interfaces() {
    echo "Checking interfaces..."
    output=$(/sbin/iw dev)
    if [[ $output =~ $WLAN0 && $output =~ $WLAN1 ]]; then
        echo "Found interfaces... continue..."
    else
        echo "Not found interfaces. check them with iwconfig"
        exit 1
    fi
}
setup_systemd_networkd() {
    sudo systemctl mask networking.service dhcpcd.service
    sudo mv /etc/network/{interfaces,interfaces~} # Backup file
    sudo cp /etc/{resolv.conf,resolv.conf~}
    sudo sed -i '1i resolvconf=NO' /etc/resolvconf.conf
    sudo systemctl enable systemd-networkd.service systemd-resolved.service
    sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
}
config_wpsup() {
    {
        echo "country=$COUNTRY"
        echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"
        echo "update_config=1"
        echo "network={"
        echo '  ssid="'${NEW_SSID}'"'
        echo "  mode=2"
        echo "  key_mgmt=WPA-PSK"
        echo '  psk="'${NEW_PASS}'"'
        echo "  frequency=2412"
        echo "}"
    } > $wp0conf
    sudo chmod 600 $wp0conf
    sudo systemctl disable wpa_supplicant.service
    sudo systemctl enable wpa_supplicant@wlan0.service
}
setup_wlan1_client() {
    {
        echo "country=$COUNTRY"
        echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev"
        echo "update_config=1"
        echo "network={"
        echo '  ssid="'$ORIGINAL_SSID'"'
        echo '  psk="'$ORIGINAL_PASS'"'
        echo '  key_mgmt=WPA-PSK'
        echo "}"
    } > $ws_wlan1

    sudo chmod 600 $ws_wlan1
    sudo systemctl disable wpa_supplicant.service
    sudo systemctl enable wpa_supplicant@wlan1.service
}
configure_interfaces() {
    {
        echo "[Match]"
        echo "Name=$WLAN0"
        echo "[Network]"
        echo "Address=192.168.$NETWORK.1/24"
        echo "IPMasquerade=yes"
        echo "IPForward=yes"
        echo "DHCPServer=yes"
        echo "[DHCPServer]"
        echo "DNS=8.8.8.8"
    } > $wlan0_network

    {
        echo "[Match]"
        echo "Name=$WLAN1"
        echo "[Network]"
        echo "DHCP=yes"
    } > $wlan1_network
}

# Config files, don't change
wp0conf="/etc/wpa_supplicant/wpa_supplicant-wlan0.conf"
ws_wlan1="/etc/wpa_supplicant/wpa_supplicant-wlan1.conf"
wlan0_network="/etc/systemd/network/08-wlan0.network"
wlan1_network="/etc/systemd/network/12-wlan1.network"

show_configurations
check_interfaces
setup_systemd_networkd
config_wpsup
setup_wlan1_client
configure_interfaces


# rm -rf $wp0conf $ws_wlan1 $wlan0_network $wlan1_network
# systemctl unmask networking.service dhcpcd.service
# mv /etc/network/{interfaces~,interfaces} # restore file
# systemctl disable systemd-networkd.service systemd-resolved.service wpa_supplicant@wlan0.service wpa_supplicant@wlan1.service
# systemctl enable wpa_supplicant.service
# rm -rf /etc/resolv.conf
# cp /etc/{resolv.conf~,resolv.conf}
# echo "done. rebooting..."
# sleep 2
# /sbin/reboot