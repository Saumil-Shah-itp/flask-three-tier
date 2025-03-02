#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
git clone https://github.com/Saumil-Shah-itp/flask-three-tier.git /home/ec2-user/flaskapp
cd /home/ec2-user/flaskapp/frontend
pip3 install flask flask-cors mysql-connector-python requests pymysql
sudo python3 /home/ec2-user/flaskapp/frontend/frontend.py
