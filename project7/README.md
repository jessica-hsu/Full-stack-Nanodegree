
sudo adduser grader
sudo nano /etc/sudoers.d/grader
  grader ALL=(ALL:ALL) ALL
sudo nano /etc/hosts
  127.0.1.1 ip-172-26-9-16

ssh -i ~/.ssh/udacity_key.pem ubuntu@18.217.94.162
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install finger
sudo dpkg-reconfigure tzdata
sudo apt-get install ntp

back to virtual
sudo mkdir /home/grader/.ssh
sudo touch /home/grader/.ssh/authorized_keys
sudo cp /root/.ssh/authorized_keys /home/grader/.ssh/authorized_keys
sudo nano /home/grader/.ssh/authorized_keys
  delete everything before 'ssh -rsa'
sudo chmod 700 /home/grader/.ssh
sudo chmod 644 /home/grader/.ssh/authorized_keys
sudo chown -R grader:grader /home/grader/.ssh

ssh -v -i ~/.ssh/udacity_key.pem grader@18.217.94.162
sudo password for grader: pass!
sudo nano /etc/ssh/sshd_config
  SET PasswordAuthentication as No
  restart
change firewall so you don't lock yourself out!
$ sudo ufw allow 2200/tcp.
$ sudo ufw allow 80/tcp.
$ sudo ufw allow 123/udp.
$ sudo ufw enable.
sudo nano /etc/ssh/sshd_config. Find the Port line and edit it to 2200
sudo service ssh restart

go to networking tab and add to firewall:
Custom TCP 2200

sudo nano /etc/ssh/sshd_config. Find the PermitRootLogin line and edit it to no.
sudo apt-get install apache2
udo apt-get install libapache2-mod-wsgi python-dev
sudo a2enmod wsgi
udo service apache2 start

sudo apt-get install git
git config --global user.name jessica-hsu
git config --global user.email hsujessica21@gmail.com
sudo cd /var/www
sudo mkdir catalog
sudo git clone https://github.com/jessica-hsu/Udacity-catalog-proj.git catalog
sudo nano catalog.wsgi

  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0, "/var/www/catalog/")

  from catalog import app as application
  application.secret_key = 'mysecret'
sudo mv application.py __init__.py
sudo apt-get install python-pip
sudo pip install virtualenv
sudo virtualenv venv
source venv/bin/activate
 sudo chmod -R 777 venv
 sudo pip install Flask -t /var/www/catalog/catalog/venv/lib/python2.7/site-packages
 sudo pip install flask_oauth -t /var/www/catalog/catalog/venv/lib/python2.7/site-packages
 sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlalchemy_utils, flask_oauth
sudo nano /etc/apache2/sites-available/catalog.conf

 <VirtualHost *:80>
    ServerName 18.217.94.162
    ServerAlias ec2-18-217-94-162.us-east-2.compute.amazonaws.com
    ServerAdmin admin@318.217.94.162
    WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/Udacity-catalog-proj/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/Udacity-catalog-proj/static
    <Directory /var/www/catalog/Udacity-catalog-proj/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

sudo service apache2 reload
sudo a2ensite catalog

sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
psql
CREATE USER catalog WITH PASSWORD 'password';
ALTER USER catalog CREATEDB;
CREATE DATABASE catalog WITH OWNER catalog;
\c catalog
REVOKE ALL ON SCHEMA public FROM public;
GRANT ALL ON SCHEMA public TO catalog;
\q
exit
sudo nano __init__.py
sudo nano database_setup.py
sudo nano database_populate.py

  change engine = create_engine... TO engine = create_engine('postgresql://catalog:password@localhost/catalog')
python /var/www/catalog/Udacity-catalog-proj/database_setup.py
python /var/www/catalog/Udacity-catalog-proj/database_populate.py
