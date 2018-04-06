#!/bin/bash

if [ -z $1 ]; then
    scriptName=`basename "$0"`
    echo  >&2 "Usage: $scriptName <tag_name>"
    exit 1
fi

# check that aws and ec2-metadata commands are installed
command -v aws >/dev/null 2>&1 || { echo >&2 'aws command not installed.'; exit 2; }
command -v ~/ec2-metadata >/dev/null 2>&1 || { echo >&2 'ec2-metadata command not installed.'; exit 3; }

# set filter parameters
instanceId=$(~/ec2-metadata -i | cut -d ' ' -f2)
filterParams=( --filters "Name=key,Values=$1" "Name=resource-type,Values=instance" "Name=resource-id,Values=$instanceId" )

# get region
region=$(~/ec2-metadata --availability-zone | cut -d ' ' -f2)
region=${region%?}

# retrieve tags
tagValues=$(aws ec2 describe-tags --output text --region "$region" "${filterParams[@]}")
if [ $? -ne 0 ]; then
    echo >&2 "Error retrieving tag value."
    exit 4
fi

# extract required tag value
tagValue=$(echo "$tagValues" | cut -f5)
echo "$tagValue"

