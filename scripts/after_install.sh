#!/bin/bash
cd /home/ec2-user/2024-October-VCT-Hackathon/
sudo pip3 install -r requirements.txt
sudo pip3 uninstall -y urllib3
sudo pip3 install urllib3
