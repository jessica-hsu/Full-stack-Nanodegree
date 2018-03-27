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
to be continued
