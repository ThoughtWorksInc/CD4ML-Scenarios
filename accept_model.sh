#!/usr/bin/env bash

# Note - not doing a `set -e` because we don't want the script to exit without displaying test failures

# export PYTHONWARNINGS="ignore::DeprecationWarning:numpy"
export PYTHONWARNINGS="ignore:numpy"

command="python3 -m pytest -k \"test_accept_model\" --cov=cd4ml --cov-report html:cov_html test"
echo "$command"
eval "$command"