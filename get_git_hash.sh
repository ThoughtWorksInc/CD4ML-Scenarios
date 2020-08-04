#!/bin/bash

gdif=`git diff`

if [ -z "$gdif" ]
then
  git rev-parse HEAD
else
  echo 'uncommitted'
fi
