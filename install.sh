#!bin/bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip libzbar0 curl -y
pip3 install --upgrade setuptools wheel
pip3 install opencv-python pyzbar
curl  https://gist.githubusercontent.com/ZusorCode/b739c6491b99e5f906af668726364aed/raw/97e43a13a18a9f0c7b759a3f4246c3858773d6ee/main.py
