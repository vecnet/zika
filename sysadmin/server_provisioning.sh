#!/usr/bin/env bash

sudo yum -y install http://lug.mtu.edu/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
sudo yum -y install http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-redhat94-9.4-2.noarch.rpm

sudo yum -y install postgresql94-server postgresql94-devel postgresql94 python-psycopg2
sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb
sudo systemctl enable postgresql-9.4
sudo sh -c 'echo "local   all             all                                     peer" > /var/lib/pgsql/9.4/data/pg_hba.conf'
sudo sh -c 'echo "host    all             all             all    md5">> /var/lib/pgsql/9.4/data/pg_hba.conf'
sudo sh -c "echo listen_addresses = \\'*\\' >> /var/lib/pgsql/9.4/data/postgresql.conf"
sudo systemctl start postgresql-9.4
sudo -u postgres sh -c '/usr/pgsql-9.4/bin/createdb zika'
# sudo -u postgres /usr/pgsql-9.4/bin/psql -c "ALTER USER postgres WITH PASSWORD '1'"
sudo -u postgres /usr/pgsql-9.4/bin/psql -c "CREATE USER zika WITH PASSWORD 'zika'"
sudo -u postgres /usr/pgsql-9.4/bin/psql -c "GRANT ALL PRIVILEGES ON DATABASE \"zika\" to zika;"
sudo systemctl restart postgresql-9.4

# Add /usr/pgsql-9.4/bin to system PATH for all users, including root and postgres
sudo sh -c 'echo "export PATH=/usr/pgsql-9.4/bin:$PATH" > /etc/profile.d/postgresql.sh'

# Install python
sudo yum -y install vim gcc git python python-devel
sudo curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo python get-pip.py
sudo rm get-pip.py
