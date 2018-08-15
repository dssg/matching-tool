#!/bin/bash

JURISDICTION=$1
MATCH_JOB=$2
CACHED_FILE_TYPE=$3


mkdir match_cache
mkdir match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}

aws s3 cp --recursive s3://dsapp-criminal-justice/csh/matcher/${JURISDICTION}/match_cache/${CACHED_FILE_TYPE}/${MATCH_JOB}/ match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}

awk 'FNR > 1 {x=FILENAME; gsub(/^(?:[^\/]*\/)+/, "", x); x+=0} {print $0, "|",  x}' match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/* > match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt

head -n 1 "match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/$(ls match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB} | head -n 1)" | sed "s/matches.*$/matches\|block/" > match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt

cat match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt > match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}.txt

rm -r match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/
rm match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt
rm match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt
