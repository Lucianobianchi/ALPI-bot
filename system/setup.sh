
# Enable EAP WiFi (@FIXME should be captive portal)
sudo cp /tmp/wpa_supplicant.conf /etc/wpa_supplicant.conf
sudo cp /tmp/interfaces /etc/network/interfaces

# Install python 
sudo apt-get install python-opencv python-serial python-picamera

pip install -r requirements.txt

sudo systemctl status dhcpd.service

sudo dhclient wlan0

# Enable camera and change password
sudo raspi-config

# Copy system service.
sudo cp neocortex /etc/init.d/neocortex

sudo chmod +x /etc/init.d/neocortex
sudo update-rc.d neocortex defaults

sudo service neocortex status
sudo service neocortex start

sudo systemctl daemon-reload

# You should see the service listed and its status
sudo service --status-all

sudo bash ./project-create.sh ALPI-bot

sudo mkdir -p /srv/tmp/
sudo chgrp -R users /srv/tmp/
sudo chmod g+w /srv/tmp/
sudo mkdir -p /srv/www/
sudo chgrp -R users /srv/www/
sudo chmod g+w /srv/www/


