#!/usr/bin/env bash

DB_NAME=zika

# http://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script
# EUID   Expands to the effective user ID of the current  user,  initialized at shell startup.
# This variable is readonly.
if [ "${EUID}" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get install -y postgresql postgresql-contrib
apt-get install -y python-pip
apt-get install -y apache2 apache2-dev

sudo -u postgres createdb ${DB_NAME}
sudo -u postgres psql -c "CREATE USER ${DB_NAME} WITH PASSWORD '${DB_NAME}'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE \"${DB_NAME}\" to ${DB_NAME};"

pip3 install mod_wsgi
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source ~/.local/bin/virtualenvwrapper.sh
