#!/bin/sh
set -eu

sudo apt-get install python3 python3-pip -y
sudo pip3 install --upgrade pip

pip3 install -r requirements.txt


cd src
Pip3 install pipenv
pip3 install django-allauth

python3 manage.py migrate
