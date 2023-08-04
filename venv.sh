#!/usr/bin/env bash

DIRECTORY=.venv
deactivate 2> /dev/null
if [ -d "${DIRECTORY}" ]; then
    source ${DIRECTORY}/bin/activate
else
    python3 -m venv ${DIRECTORY}
    source ${DIRECTORY}/bin/activate
fi
