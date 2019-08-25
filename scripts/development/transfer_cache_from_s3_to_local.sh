#!/bin/bash

###############################################################################
# This script is useful for reading from S3 and concatenating cached files    #
# from a match job that are stored as one file per block (contrasts, raw      #
# cluster ids, and squared distance matrices).                                #
#                                                                             #
# The script requires that the AWS command line script is installed and       #
# configured.                                                                 #
#                                                                             #
# To run the script, pass the following command line arguments:               #
#                                                                             #
#   1. BASE_PATH: the base S3 storage path                                    #
#   2. JURISDICTION: the short name of the jurisdiction                       #
#   3. MATCH_JOB: the id of the match job you want to investigate (can be     #
#      found in the match_log table in the database)                          #
#   4. CACHED_FILE_TYPE: the type of matcher cache output (contrasts,         #
#      raw_cluster_ids, or square_distances) you would like to read           #
#                                                                             #
# Warning: The script will create the match_cache directory and store the     #
# data, which includes personally identifying information, in the directory   #
# where it is run. It is recommended to run it from outside the repo to avoid #
# mistakenly committing any sensitive information.                            #
###############################################################################

# Assign arguments to named variables
BASE_PATH=$1
JURISDICTION=$2
MATCH_JOB=$3
CACHED_FILE_TYPE=$4

# Make directories to store final and temporary files
mkdir match_cache
mkdir match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}

# Copy all of the block files to local directory
aws s3 cp --recursive s3://${BASE_PATH}/${JURISDICTION}/match_cache/${CACHED_FILE_TYPE}/${MATCH_JOB}/ match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}

# Add the filename (block name) as a final column to all rows after the first
# (header) and concatenate all of the files
awk 'FNR > 1 {x=FILENAME; gsub(/^(?:[^\/]*\/)+/, "", x); x+=0} {print $0, "|",  x}' match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/* > match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt

# Grab the header row form the first block's file and add the column header
# "block"; save the result to a temporary file
head -n 1 "match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/$(ls match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB} | head -n 1)" | sed "s/matches.*$/matches\|block/" > match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt

# Concatenate the header and the rows files
cat match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt > match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}.txt

# Clean up temporary files
rm -r match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}/
rm match_cache/${CACHED_FILE_TYPE}_column_names_${MATCH_JOB}.txt
rm match_cache/${CACHED_FILE_TYPE}_all_blocks_${MATCH_JOB}.txt

# Notify user
echo "Your file is ready at match_cache/${CACHED_FILE_TYPE}_${MATCH_JOB}.txt"

