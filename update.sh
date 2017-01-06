#!/usr/bin/env bash

function update
{
    echo "--------------- Starting update ---------------"
    git pull
    pip3 install -r requirements/prod.txt
    python3 manage.py migrate
    python3 manage.py collectstatic --noinput
    touch wsgi.py
    python3 manage.py check --deploy
    echo "--------------- Update complete ---------------"
}

# Append output of update command to the beginning of update.log flie
mv update.log update.log.bak
update | tee update.log
cat update.log.bak >> update.log
