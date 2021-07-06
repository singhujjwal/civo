#!/bin/bash
sudo yum -y update
sudo yum groupinstall "Development Tools" -y
sudo yum install openssl-devel libffi-devel bzip2-devel -y
sudo yum install wget -y
wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz
tar xvf Python-3.9.5.tgz
cd Python-3.9*/
./configure --enable-optimizations
sudo make altinstall

pip3.9  install virtualenv

echo 'alias c=clear' >> ~/.bashrc
echo 'alias k=kubectl' >> >> ~/.bashrc

#python3.9 -m virtualenv ~/.p39
#source ~/.p39/bin/activate
#ssh-keygen

