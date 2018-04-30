#!bin/bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip libzbar0 curl -y
pip3 install --upgrade setuptools wheel
pip3 install opencv-python pyzbar
