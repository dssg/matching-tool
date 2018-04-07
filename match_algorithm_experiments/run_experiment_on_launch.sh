#!/bin/bash

# set up environment
ln -s -f /usr/bin/python3 /usr/bin/python
apt-get -y install python3-pip
pip3 install awscli
git config --global credential.helper --file ~/.git-credentials
git config --global user.name 'csh-matcher'
sed '2,$ s/^/export /' /etc/environment | source /dev/stdin

cd ~

branch=$(./get-tag.sh branch)
jurisdiction=$(./get-tag.sh jurisdiction)
file=$(./get-tag.sh file)

# set up repo
git clone https://github.com/dssg/csh
cd csh
git checkout ${branch}
aws s3 cp s3://dsapp-criminal-justice/csh/docker_compose_files/${file} docker-compose.yml

# run the match
./csh.sh rebuild
./csh.sh start
http 0.0.0.0:5001/match/${jurisdiction}/jail_bookings uploadId==${file}

