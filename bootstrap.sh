#!/bin/bash

virtualenv .
. ./bin/activate

pip install -r ./requirements.txt

cd flangular/static
bower install

cd -

echo -e "\e[00;32mFlangular has been set up. \e[00m\nTry running: ./server.py"
