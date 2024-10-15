#!/bin/bash
cd /home/ec2-user/2024-October-VCT-Hackathon/
sudo nohup python3 -m waitress --host=0.0.0.0 --port=5001 project.app:app > waitress_out.txt 2>&1 &
