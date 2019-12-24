#!/bin/bash
cd "${BASH_SOURCE%/*}/"

echo " > Running unit tests..."
python3 pylinquery_tests/enumerable_tests.py