#!/bin/bash

# set up environment
export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate csh-matcher
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
./csh.sh start
http 0.0.0.0:5001/match/${jurisdiction}/jail_bookings uploadId==${file}

