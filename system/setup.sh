
# Enable EAP WiFi (@FIXME should be captive portal)
sudo cp /tmp/wpa_supplicant.conf /etc/wpa_supplicant.conf
sudo cp /tmp/interfaces /etc/network/interfaces

# Install python 
sudo apt-get install python-opencv python-serial python-picamera


sudo systemctl status dhcpd.service

sudo dhclient wlan0

# Enable camera and change password
sudo raspi-config

# Copy system service.
sudo cp /tmp/neocortex /etc/init.d/neocortex

sudo service neocortex status
sudo service neocortex start

sudo systemctl daemon-reload neocortex
