#!/bin/bash

# you may need to change this path
SCRIPT='./wiki_edits.py --meta --language polish'

# check prerequisities
if [ $# -ne 3 ]; then
  echo "three arguments required"
  echo "usage: $0 working-directory edits-dir dump-url"
  exit 1
fi

WORK_DIR=$1
EDITS_DIR=$2
URL=$3
DIR=`pwd`


cd ${WORK_DIR}
echo "working directory is" `pwd`
mkdir -p ${EDITS_DIR}

# download wiki dump
BASENAME=`basename "${URL}" .7z`
DUMP_FILE="${BASENAME}.7z"

if [ ! -f $DUMP_FILE ]
then
  wget -nc ${URL}
else
  echo "dump file ${DUMP_FILE} exists"
fi

# extract editions
EDIT_FILE="${EDITS_DIR}/${BASENAME}.txt"

if [ ! -f $EDIT_FILE ]
then
  7zr e -so ${DUMP_FILE} | ${SCRIPT} > ${EDIT_FILE}
else
  echo "file with editions ${EDIT_FILE} exists"
fi

# go back
cd ${DIR}
