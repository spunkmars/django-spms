#!/bin/sh

PYTHON3_PROG='/data/packages/vpython36/bin/python'
PYTHON2_PROG='/data/packages/vpython27/bin/python'

if [[ $1 == '3' ]];then
    PYTHON_PROG=${PYTHON3_PROG}
else
    PYTHON_PROG=${PYTHON2_PROG}
fi
${PYTHON_PROG} setup.py sdist