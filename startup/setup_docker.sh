#!/bin/bash

# Run using the below command
# bash vm_setup.sh

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing  packages..."
sudo apt-get -y install docker.io

echo "Adding Docker official GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
 
echo "Setting up repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Running sudo apt-get update..."
sudo apt-get update

echo "Installing latest docker..."
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Docker without sudo setup..."
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart

echo "Setup .bashrc..."
echo '' >> ~/.bashrc
echo 'export PATH=${HOME}/bin:${PATH}' >> ~/.bashrc
eval "$(cat ~/.bashrc | tail -n +10)" # A hack because source .bashrc doesn't work inside the script

echo "docker version..."
docker --version

mkdir -p ~/.google/credentials