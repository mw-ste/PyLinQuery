#!/bin/bash
cd "${BASH_SOURCE%/*}/"

echo " > Building python wheel..."
python3 setup.py bdist_wheel > /dev/null
cp dist/pylinquery-*-py3-none-any.whl .

echo " > Cleaning up build artifacts..."
rm -rf build
rm -rf dist
rm -rf pylinquery.egg-info

echo " > Installing wheel..."
pip install --upgrade pylinquery-*-py3-none-any.whl