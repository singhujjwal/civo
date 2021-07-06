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

KUBECTL_VERSION="v1.19.6"
sudo curl -LsSO https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl
sudo chmod +x kubectl
sudo mv kubectl /usr/local/bin/


TF_VERSION=1.0.1
wget https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_linux_amd64.zip
unzip terraform_${TF_VERSION}_linux_amd64.zip
sudo mv terraform /usr/local/bin/terraform
rm terraform_${TF_VERSION}_linux_amd64.zip
#terraform --version                       

sudo wget https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator
sudo chmod +x ./aws-iam-authenticator
sudo mv ./aws-iam-authenticator /usr/local/bin/


export TERRAGRUNT_VERSION="0.23.13"
wget https://github.com/gruntwork-io/terragrunt/releases/download/v${TERRAGRUNT_VERSION}/terragrunt_linux_amd64
sudo mv terragrunt_linux_amd64 /usr/local/bin/terragrunt
sudo chmod +x /usr/local/bin/terragrunt

sudo yum install jq -y


# Tmux
sudo yum remove -y tmux
sudo yum install -y libevent-devel ncurses-devel
wget https://github.com/tmux/tmux/releases/download/2.9/tmux-2.9.tar.gz
tar -zxvf tmux-2.9.tar.gz
cd tmux-2.9
./configure
make
sudo cp tmux /usr/bin/tmux
cd ~
rm -rf tmux-2.9.tar.gz tmux-2.9
tmux -V
HOME=/home/centos
tee ${HOME}/.tmux.conf <<EOF
set-window-option -g mode-keys vi
set-option -g history-limit 50000
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
bind r source-file ~/.tmux.conf \; display-message "Config reloaded..."
set -g base-index 1
setw -g pane-base-index 1
set -g status-left-length 100
set -g status-left " "
set -g status-justify "left"
set -g status-right ""
set -g automatic-rename on
setw -g window-status-current-format '#I:#{pane_current_path}*'
setw -g window-status-format '#I:#{pane_current_path}'
EOF



echo 'alias c=clear' >> ~/.bashrc
echo 'alias k=kubectl' >> >> ~/.bashrc

#python3.9 -m virtualenv ~/.p39
#source ~/.p39/bin/activate
#ssh-keygen

