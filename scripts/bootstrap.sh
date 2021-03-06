#!/bin/bash
#
# Bootstrap virtualenv environment and postgres databases locally.
#
# NOTE: This script expects to be run from the project root with
# ./scripts/bootstrap.sh

set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

if [ ! $VIRTUAL_ENV ]; then
  virtualenv ./venv
  . ./venv/bin/activate
fi

# Some of the specified packages use syntax in their requirements.txt
# that older pips don't understand
pip install "pip>=8.0"

# Install Python development dependencies
pip install -r requirements_for_test.txt

# Create Postgres databases
createdb digitalmarketplace
createdb digitalmarketplace_test

# Upgrade databases
python application.py db upgrade
