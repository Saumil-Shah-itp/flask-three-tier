#!/bin/bash
yum update -y
yum install -y python3 python3-pip git
git clone https://github.com/Saumil-Shah-itp/flask-three-tier.git /home/ec2-user/flaskapp
cd /home/ec2-user/flaskapp/backend
sudo pip3 install flask flask-cors mysql-connector-python requests pymysql
sudo pip3 install --upgrade urllib3==1.26.16
sudo python3 /home/ec2-user/flaskapp/backend/backend.py 
