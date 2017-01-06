# Deployment guide - Linux/RedHat 7 

1. Provision server

```bash
$SITE=/opt/portal/zika.vecnet.org
$WORKON_HOME=/opt/portal/venv
sudo mkdir -p "$WORKON_HOME"
sudo mkdir -p "$SITE"
sudo chown $USER "$SITE"
cd "$SITE"
git clone https://github.com/vecnet/zika.git .
bash server/server_provisioning.sh
```

2. Deploy source code

```bash
export HOSTNAME=wellbeing-portal-test
export SITE=/opt/portal/$HOSTNAME.crc.nd.edu
sudo mkdir -p $SITE
sudo chown $USER:apache $SITE
chmod 750 $SITE
cd $SITE
git clone https://github.com/crcresearch/wellbeingatwork.git .
# Switch to a branch if necessary
git fetch origin
git branch -v -a
git checkout -b user_portal origin/user_portal

sudo -u postgres sh -c '/usr/pgsql-9.4/bin/createdb $HOSTNAME'
sudo -u postgres /usr/pgsql-9.4/bin/psql -c "CREATE USER \"$HOSTNAME\" WITH PASSWORD '$HOSTNAME'"
# sudo -u postgres /usr/pgsql-9.4/bin/psql -c "DROP ROLE \"$HOSTNAME\""
# sudo -u postgres /usr/pgsql-9.4/bin/createuser -P wellbeing-portal-test
sudo -u postgres /usr/pgsql-9.4/bin/psql -c "GRANT ALL PRIVILEGES ON DATABASE \"$HOSTNAME\" to \"$HOSTNAME\";"

mkvirtualenv $HOSTNAME
pip install -r requirements.txt
vim website/settings_local.py
fab update
```


3. Create apache virtual host

Example apache virtual host configuration is below. Replace "wellbeing.crc.nd.edu" with actual hostname
```apache
<VirtualHost *:80>
  ServerName wellbeing.crc.nd.edu 
  RewriteEngine On
  RewriteCond %{HTTPS} off
  RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}?%{QUERY_STRING}
</VirtualHost>

<VirtualHost *:443>
  ServerAdmin avyushko@nd.edu
  ServerName wellbeing.crc.nd.edu
  CustomLog /var/log/httpd/wellbeing.crc.nd.edu.access.log combined
  ErrorLog /var/log/httpd/wellbeing.crc.nd.edu.error.log

  DocumentRoot "/opt/portal/wellbeing.crc.nd.edu/"
  Alias /static/ /opt/portal/wellbeing.crc.nd.edu/apache/static/
  <Directory /opt/portal/wellbeing.crc.nd.edu/apache/static/ >
    # Order deny,allow
    # Allow from all
    Require all granted
  </Directory>

  <Directory "/opt/portal/wellbeing.crc.nd.edu/">
    Options Includes FollowSymLinks
    AllowOverride all
    # Order allow,deny
    # Allow from all
    Require all granted
  </Directory>

  WSGIDaemonProcess wellbeing processes=3  python-path=/opt/portal/wellbeing.crc.nd.edu/:/opt/venv/wellbeing.crc.nd.edu/lib/python2.7/site-packages:/usr/lib/python2.7/ home=/opt/portal/wellbeing.crc.nd.edu/  display-name=httpd-wellbeing
  WSGIProcessGroup wellbeing
  WSGIScriptAlias / /opt/portal/wellbeing.crc.nd.edu/wsgi.py

  <Directory "/var/www/icons">
    Options Indexes MultiViews FollowSymLinks
    AllowOverride None
    # Order allow,deny
    # Allow from all
    Require all granted
  </Directory>

  SSLEngine on
  SSLCertificateFile /etc/httpd/ssl/wellbeing.crc.nd.edu.cer
  SSLCertificateKeyFile /etc/httpd/ssl/wellbeing.crc.nd.edu.key
  SSLCertificateChainFile /etc/httpd/ssl/wellbeing.crc.nd.edu.int.cer

</VirtualHost>
```

Use sed command to generate new virtual host config file

```bash
cat zika.vecnet.org.conf | sed s/wellbeing.crc.nd.edu/zika.vecnet.org/
```


4. Follow deployment checklist in README.md

5. Create database structures
    `./manage.py migrate`

6. Check if there are database migrations by reviewing the list of known migrations:
    `./manage.py migrate --list`

7. Install logwatch
```bash
sudo apt-get install logwatch
```

For postfix configuration, choose "smarthost" and specify smtp.nd.edu as relay host

8. Configure logwatch: /etc/logwatch/conf/logwatch.conf file
```
MailTo = avyushko@nd.edu
MailFrom = avyushko+zika@nd.edu
Detail = High
```