#!/usr/bin/env bash

git pull
pip3 install -r requirements/prod.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch wsgi.py