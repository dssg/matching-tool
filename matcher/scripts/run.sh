#!/bin/bash

JURISDICTION=$1

UPLOAD_ID=$3

http 0.0.0.0:5001/match/${JURISDICTION}/$2 uploadId==${UPLOAD_ID}
