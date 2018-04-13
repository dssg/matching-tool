#!/bin/bash

JURISDICTION=$1

EVENT_TYPE=$2

UPLOAD_ID=$3

cd csh
apt-get update && apt-get install -y curl && curl --silent https://bootstrap.pypa.io/get-pip.py |python3 && pip install --upgrade httpie
pip3 install httpie
# apt-get update && apt-get install -y curl && curl --silent https://bootstrap.pypa.io/get-pip.py |python3 && pip install --upgrade httpie
echo ${JURISDICTION}
echo ${EVENT_TYPE}
echo ${UPLOAD_ID}

# TODO: We still need to login to each machine and run go.sh manually.
echo http 0.0.0.0:5001/match/${JURISDICTION}/${EVENT_TYPE}/filename uploadId==${UPLOAD_ID} > /home/ubuntu/go.sh
# http 0.0.0.0:5001/match/${JURISDICTION}/${EVENT_TYPE}/filename uploadId==${UPLOAD_ID}
chmod u+x /home/ubuntu/go.sh

echo done
