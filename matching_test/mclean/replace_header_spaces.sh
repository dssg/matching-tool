#!/bin/bash

# This script iterates through all .csvs in the current directory and replaces
# any spaces on the first line of the file with underscores and removes any
# question marks or periods in the first line.

for file in *.csv
do 
    {
        echo replacing spaces and removing punctuation marks in ${file}
        sed -i '1s/\ /_/g' ${file}
        sed -i '1s/[\?\.]//g' ${file}
    }
done
