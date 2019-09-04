1. "APScript" is used for setting up a Raspberry Pi as a Wireless Access Point, The IP address, ssid and wpa_passphrase may be changed. First, check the configuration of /etc/network/interfaces by cmd: sudo nano /etc/network/interfaces, then press Ctrl+X to exit
# interfaces(5) file used by ifup(8) and ifdown(8)
# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'
# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

Then, run
sudo chmod 777 APScript
sudo ./APScript
