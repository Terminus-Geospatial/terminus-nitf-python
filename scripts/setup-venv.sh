#!/usr/bin/env bash
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#*                                                                                    *#
#*                           Copyright (c) 2025 Terminus LLC                          *#
#*                                                                                    *#
#*                                All Rights Reserved.                                *#
#*                                                                                    *#
#*          Use of this source code is governed by LICENSE in the repo root.          *#
#*                                                                                    *#
#**************************** INTELLECTUAL PROPERTY RIGHTS ****************************#
#

set -e

function check_python_version() {

    PYVERSION="$(python3 --version | awk '{print $2}' )"
    PYVERSION2="$( echo ${PYVERSION} | sed 's/\./ /g' )"
    
    PYVERSION_MAJOR="$(echo ${PYVERSION2} | awk '{ print $1 }' )"
    PYVERSION_MINOR="$(echo ${PYVERSION2} | awk '{ print $2 }' )"

    if [ "${PYVERSION_MAJOR}" != '3' ]; then
        echo "Must use Python 3."
        exit 1
    fi
    if [ "${PYVERSION_MINOR}" -lt 11 ]; then
        echo "Must use at least Python version 3.11. Current: ${PYVERSION}"
        exit 1
    fi
    echo "Python Version: [${PYVERSION}] Installed"
}


if [ ! -d './.git' ]; then 
    echo 'Run this script from the base repo folder!'
    exit 1
fi

#  Check the version
check_python_version

#  Create venv
python3 -m venv venv

#  Activate Virtual Environment
. venv/bin/activate

#  Run pip install upgrade
pip install --upgrade pip
pip install build

#  Build Wheel
python -m build

