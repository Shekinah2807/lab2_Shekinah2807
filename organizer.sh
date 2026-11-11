#!/bin/bash

if [ ! -d "archive" ]; then
    mkdir archive
fi

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

if [ -f "grades.csv" ]; then
    ARCHIVED_NAME="archive/grades_${TIMESTAMP}.csv"
    mv grades.csv "$ARCHIVED_NAME"
    touch grades.csv

    LOG_ENTRY="[${TIMESTAMP}] Archived grades.csv to ${ARCHIVED_NAME}"
    echo "$LOG_ENTRY" >> organizer.log
    echo "Success: $LOG_ENTRY"
else
    echo "Error: grades.csv does not exist in the current directory."
    exit 1
fi
