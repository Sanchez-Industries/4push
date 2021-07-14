#!/usr/bin/bash
echo "Start Update..."
cd /tmp
git clone https://gitlab.com/opensource-university/4push.git
cd 4push
sudo bash install.sh
cd /tmp/
sudo rm -r 4push/
cd ~
echo "OK."