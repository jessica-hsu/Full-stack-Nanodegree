# Full-stack-Nanodegree

**UPDATE #1** <br>
I deleted the linux instance from AWS Lightsail a few days after completing the nanodegree. The application URL and IP address will no longer work. <br>

**UPDATE #2** <br>
README has been updated with a walkthrough of how I completed the project. Special thanks to the README authors listed below. <br>

## Project 7: Linux Server Configuration
**Project Description** (from Udacity):
>You will take a baseline installation of a Linux server and prepare it to host your web applications. You will secure your server from a number of attack vectors, install and configure a database server, and deploy one of your existing web applications onto it.

### IP Address, SSH Port, Grader Login, Application URL
**Public IP Address:** 18.217.94.162 <br>
**SSH Port:** 2200 <br>
**SSH login as Grader**: ssh -v -i ~/.ssh/udacity_key.pem grader@18.217.94.162 -p 2200 <br>
**Application URL:** [http://ec2-18-217-94-162.us-east-2.compute.amazonaws.com](http://ec2-18-217-94-162.us-east-2.compute.amazonaws.com)
<br>

### Software Installed & Configuration Changes
**Software Installed:** <br>
Finger, Daemon NTPD, Apache2, Unattended Upgrades, Mod_wsgi (Apache HTTP server mod), Git, Pip, Flask, Virtualenv, Flask_oauth, httplib2, sqlalchemy, psycopg2, sqlalchemy_utils, Postgres, libpq-dev, Python
<br><br>
**Configuration Changes:** <br>
1) Added grader, gave grader sudo permissions, and changed root owner to Grader <br>
2) Timezone configured to UTC <br>
3) Keys configured for grader <br>
4) Enforced key-based authentication <br>
5) Changed port from 22 to 2200 <br>
6) Added firewall permissions for SSH port 2200, HTTP port 80, NTP port 123 <br>
7) Disabled ssh login for root/ubuntu user <br>
8) Configured virtual host and PostgreSQL for catalog app

### Third Party Resources
**Major special thanks to these people for their <i>extremely</i> helpful README:** </br>
[SteveWooding](https://github.com/SteveWooding/fullstack-nanodegree-linux-server-config),
[iliketomatoes](https://github.com/iliketomatoes/linux_server_configuration),
[stueken](https://github.com/stueken/FSND-P5_Linux-Server-Configuration),
[rrjoson](https://github.com/rrjoson/udacity-linux-server-configuration),
[anumsh](https://github.com/anumsh/Linux-Server-Configuration)

### Tutorial (based on a combination of the five tutorials above)
#### Setting up the Linux Instance ...
1) Follow the Amazon Lightsail instructions on Udacity <br>
2) Login to the instance via web browser or command line <br>
2a) Connect with Web Browser: Just click 'Connect via SSH' on the lightsail website when you click into the Instance <br>
2b) Connect with Terminal/Command Line: Download the private key. Locate the private key file in your Downloads foler and rename to udacity_key (file extention is either .rsa or .pem). Move your private key file to ~/.ssh/ directory. You can now connect via terminal with:
```
bash-3.2$ ssh -i ~/.ssh/udacity_key.pem ubuntu@[YOUR.PUBLIC.IP.ADDRESS]
```
#### Install updates/upgrades and fix timezone
1) Login to virtual machine (VM) <br>
2) Update and upgrade everything:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install finger
sudo apt-get install ntp
```
3) Change timezone to UTC (pick UTC after typing in command)
```
sudo dpkg-reconfigure tzdata
```
#### Add user and configure permissions & login stuff for Grader
1) Add new user 'grader' and give it sudo permissions
```
sudo adduser grader
sudo nano /etc/sudoers.d/grader
```
1a) Type ```grader ALL=(ALL:ALL) ALL``` in the sudoer.d/grader file you opened. Save it <br>
1b) Run the command ```sudo nano /etc/hosts``` and add ```127.0.1.1 ip-[private]-[ip]-[address]``` (example: mine is ip-172-26-9-16) to prevent a host permissions error <br>
2) SSH login for grader
```
sudo mkdir /home/grader/.ssh
sudo touch /home/grader/.ssh/authorized_keys
sudo cp /root/.ssh/authorized_keys /home/grader/.ssh/authorized_keys
sudo nano /home/grader/.ssh/authorized_keys
 (delete everyting before 'ssh -rsa' so that only the key remains)
sudo chmod 700 /home/grader/.ssh
sudo chmod 644 /home/grader/.ssh/authorized_keys
```
3) Give root ownership to grader and restart
```
sudo chown -R grader:grader /home/grader/.ssh
sudo service ssh restart
```
4) Check that you can login with grader account
```
ssh -v -i ~/.ssh/udacity_key.pem grader@PUBLIC.IP.ADDRESS
```
#### Configure firewall, ports, and other permissions
1) Login as grader with ```ssh -v -i ~/.ssh/udacity_key.pem grader@PUBLIC.IP.ADDRESS``` <br>
2) Note: if you sudo and system asks for sudo password for grader, use the UNIX password you entered when creating the user 'grader' <br>
3) Turn off password authentication
```
sudo nano /etc/ssh/sshd_config
```
3a) Find PasswordAuthentication and set as No.
4) Configure firewall to allow certain port numbers and port types
```
sudo ufw allow 2200/tcp
sudo ufw allow 80/tcp
sudo ufw allow 123/upd
sudo ufw enable
```
4a) Go to your instance web page and find the Networking tab. Add to firewall: Custom TCP 2200 <br>
5) Change port number for Login
```
sudo nano /etc/ssh/sshd_config
```
5a) Find the port line and add Port 2200. Keep Port 22 for now. Restart with ```sudo service ssh restart```. Open another command line window and try to login with grader using port 2200 with ```ssh -v -i ~/.ssh/udacity_key.pem grader@public.ip.address -p 2200```. If this works, then go back to /etc/ssh/sshd_config and you can remove Port 22 and keep port 2200 only. <br>
6) Remove root Login. Type command ```sudo nano /etc/ssh/sshd_config``` and find PermitRootLogin and set it as No. Restart system.
6a) Try to login as ubuntu/root. If you can still login, then add DenyUsers ubuntu to the sshd_config file. Test again <br>

#### Install and Configure everything you need to upload your catalog project to your Linus Server
