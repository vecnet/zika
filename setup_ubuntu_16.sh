#!/usr/bin/env bash

DB_NAME=zika
APACHE=www-data

# http://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script
# EUID   Expands to the effective user ID of the current  user,  initialized at shell startup.
# This variable is readonly.
if [ "${EUID}" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get update
apt-get install -y postgresql postgresql-contrib libpq-dev
apt-get install -y python3-pip git
apt-get install -y apache2 apache2-dev

sudo -u postgres createdb ${DB_NAME}
sudo -u postgres psql -c "CREATE USER ${DB_NAME} WITH PASSWORD '${DB_NAME}'"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE \"${DB_NAME}\" to ${DB_NAME};"

#################################
# Configure apache
#################################
pip3 install mod_wsgi
# Refer to https://pypi.python.org/pypi/mod_wsgi for additional information
echo `mod_wsgi-express module-config` > /etc/apache2/mods-available/mod_wsgi.conf
# Manually edit /etc/apache2/mods-available/mod_wsgi.conf
service apache2 restart

#################################
# Configure python and virtualenvwrapper
#################################
# Note that command below should run as root
pip3 install virtualenvwrapper
mkdir -p /opt/venv
sudo chown $USER:$APACHE /opt/venv
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
WORKON_HOME=/opt/venv
source /usr/local/bin/virtualenvwrapper.sh

cat > /etc/profile.d/venv.sh << EOL
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
WORKON_HOME=/opt/venv
source /usr/local/bin/virtualenvwrapper.sh
EOL

mkvirtualenv $SITE_URL

#############################
# Configure Django application
#############################
DIR=/opt/portal/$SITE_URL
 if [ ! -d "$DIR" ]; then
    sudo mkdir -p "$DIR"
    sudo chown $USER:$APACHE "$DIR"
    git clone https://github.com/vecnet/zika.git "$DIR"
    if [ ! "$?" -eq 0 ]; then
       # You're going to see exit code 1 for errors, and 0 for success.
       # If error happened, it is likely to be wrong username or password
       echo "Try again"
       git clone https://github.com/vecnet/zika.git "$DIR"
    fi
    workon $SITE_URL
    pip3 install -r $DIR/requirements/prod.txt
    cat > $DIR/website/settings_local.py << EOL
DEBUG=False
SECRET_KEY="aaaa"
HOSTS_ALLOWED = ('$SITE_URL', )
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$DB_NAME',
        'USER': '$DB_NAME',
        'PASSWORD': '$DB_NAME',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
EOL
    cat $DIR/website/settings_local.py
    cd $DIR
    touch $DIR/django.log
    fab update
    mkdir -p $DIR/logs
    chown -R $USER:$APACHE $DIR
    chmod g+w $DIR/logs
else
    echo "Cowardly refusing to clobber $DIR directory."
fi


#############################
# Configure apache - SSL
#############################
echo "Configuring apache"
a2enmod rewrite
a2enmod ssl

mkdir -p /etc/apache2/ssl/
cat > /etc/apache2/sites-available/$SITE_URL.conf << EOL
<VirtualHost *:80>
  ServerName $SITE_URL
  Alias /.well-known/ /opt/portal/$SITE_URL/apache/.well-known/
  RewriteEngine On
  RewriteCond %{HTTPS} off
  # Leave /.well-known/ directory open for let's encrypt it client
  RewriteCond %{REQUEST_URI} !^/.well-known
  RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}?%{QUERY_STRING}

  <Directory /opt/portal/$SITE_URL/apache/.well-known/>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
  </Directory>


</VirtualHost>

<VirtualHost *:443>
  ServerAdmin avyushko@nd.edu
  ServerName $SITE_URL
  CustomLog /opt/portal/$SITE_URL/logs/$SITE_URL.access.log combined
  ErrorLog /opt/portal/$SITE_URL/logs/$SITE_URL.error.log

  SSLEngine on

  SSLCipherSuite HIGH:MEDIUM:!aNULL:!MD5:!RC4
  SSLCertificateFile /etc/apache2/ssl/$SITE_URL.crt
  SSLCertificateKeyFile /etc/apache2/ssl/$SITE_URL.key
  SSLCertificateChainFile /etc/apache2/ssl/$SITE_URL.int.cer


  DocumentRoot "/opt/portal/$SITE_URL/"
  Alias /static/ /opt/portal/$SITE_URL/apache/static/
  <Directory /$SITE_URL/apache/static/ >
    # Order deny,allow
    # Allow from all
    Require all granted
  </Directory>

  <Directory "/opt/portal/$SITE_URL/">
    Options Includes FollowSymLinks
    AllowOverride all
    # Order allow,deny
    # Allow from all
    Require all granted
  </Directory>

  WSGIDaemonProcess $SITE_URL processes=3  python-path=/opt/portal/$SITE_URL/:/opt/venv/$SITE_URL/lib/python3.5/site-packages:/usr/lib/python3.5/ home=/opt/portal/$SITE_URL/  display-name=$SITE_URL
  WSGIProcessGroup $SITE_URL
  WSGIScriptAlias / /opt/portal/$SITE_URL/wsgi.py

  TraceEnable Off

</VirtualHost>
EOL

a2ensite $SITE_URL.conf

##########################
# Firewall configuration
##########################
ufw allow http
ufw allow https


##########################
# Let's encrypt it
##########################
sh -c "curl https://get.acme.sh | sh"
/root/.acme.sh/acme.sh --issue -d zika.vecnet.org -w /opt/portal/zika.vecnet.org/apache
/root/.acme.sh/acme.sh --installcert -d zika.vecnet.org --certpath /etc/apache2/ssl/zika.vecnet.org.cer --keypath /etc/apache2/ssl/zika.vecnet.org.key --fullchainpath /etc/apache2/ssl/zika.vecnet.org.int.cer --reloadcmd "service apache2 restart"
