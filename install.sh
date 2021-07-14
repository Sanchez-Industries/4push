#!/usr/bin/bash
echo "Start Install..."
echo "install file2b64..."
sudo cp scripts/file2b64.py /usr/bin/file2b64
sudo chmod a+x /usr/bin/file2b64
#==================================================
echo "install capsule-machine..."
sudo cp scripts/capsule-machine.py /usr/bin/capsule-machine
sudo chmod a+x /usr/bin/capsule-machine
#==================================================
echo "install defaults..."
sudo mkdir -p /var/4push/defaults/
sudo file2b64 src/defaults/4push.json -o /var/4push/defaults/4push.json.b64
sudo file2b64 src/defaults/4push.txt -o /var/4push/defaults/4push.txt.b64
sudo chmod a+r /var/4push/defaults/4push.json.b64
sudo chmod a+r /var/4push/defaults/4push.txt.b64
#==================================================
echo "install 4push..."
sudo cp src/4push.py /usr/bin/4push
sudo chmod a+x /usr/bin/4push
#==================================================
echo "Done."