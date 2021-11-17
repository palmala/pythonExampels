#!/bin/bash

cat example.txt 2>/dev/null
if [ "$?" -ne "0" ]
then
  >&2 echo "ERROR: File is missing!"
fi
