#! /bin/bash
sudo yum update -y
sudo yum install git -y
#sudo yum install nmap -y
cd /home/ec2-user && git clone https://github.com/juansedo/tet-challenge1.git
cd /home/ec2-user/ && chmod -R 777 tet-challenge1/
cd /home/ec2-user/tet-challenge1/hermes-server && pip3 install requests