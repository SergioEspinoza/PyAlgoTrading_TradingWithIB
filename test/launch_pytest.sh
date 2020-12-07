#!/usr/bin/bash

#Add parent directory to PYTHONPATH
#so 'screeners' module can be imported without installing it
if [ -z $PYTHONPATH ]; then
  echo "PYTHONPATH empty"
  export PYTHONPATH="$(pwd)/.."
  echo "new PYTHONPATH: $PYTHONPATH"
elif [[ ":$PYTHONPATH:" != *":$(pwd):"* ]]; then
  echo "PYTHONPATH not empty"
  export PYTHONPATH="$PYTHONPATH:$(pwd)/.."
fi

if [ -z $1 ]; then
  echo "executing all unit tests"
  pytest --lo-cli-level="INFO" -s
else
  echo "executing unit tests marked as: $1"
  pytest --log-cli-level="INFO" -m ${1} -s
fi
