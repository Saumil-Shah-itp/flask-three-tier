#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
pip3 install flask flask-cors mysql-connector-python requests pymsql
cd /home/ec2-user/flaskapp/backend/
python3 /home/ec2-user/flaskapp/backend/backend.py
