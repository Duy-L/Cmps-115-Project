#!/bin/sh
set -eu

sudo apt-get install python3 python3-pip -y
sudo pip3 install --upgrade pip

pip3 install -r requirements.txt
pip3 install django-allauth
Brew install postgres
Pip3 install psycopg2
pip3 install django psycopg2 dj-database-url gunicorn

cd src
python3 manage.py migrate
