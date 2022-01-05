#!/usr/bin/env bash

# Note - not doing a `set -e` because we don't want the script to exit without displaying test failures

export PYTHONWARNINGS="ignore:numpy"

command="python3 -m pytest --cov=cd4ml --cov-report html:cov_html test"

echo "$command"
eval "$command"

echo
echo Flake8 comments:
# extend-ignore T0001 ignores print() statements in project
flake8 --extend-ignore T001 --max-line-length=120 cd4ml
