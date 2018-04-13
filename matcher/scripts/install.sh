#!/bin/bash

GITHUB_USER=
GITHUB_PASSWORD=

export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

echo "Installing needed dependencies"
sudo add-apt-repository 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
  sudo apt-key add -
sudo apt-get update
sudo apt-get install -y python3-pip postgresql-client-10

echo "Installing awscli and httpie"
pip3 install awscli httpie

echo "Installing docker-compose"
sudo curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Cloning CSH repository"
git clone https://${GITHUB_USER}:${GITHUB_PASSWORD}@github.com/dssg/csh.git

echo "Building the infrastructure"
cd csh
# TODO: this will need to be removed before merging
git checkout environment_file

echo "Copying the environment file to the repo"
mv _env .env

echo "Running the infrastructure"

./csh.sh build db redis matcher matcher_worker
./csh.sh start db redis matcher matcher_worker

