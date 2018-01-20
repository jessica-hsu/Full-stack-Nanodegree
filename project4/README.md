# Full-stack-Nanodegree
## Project 4: Design A Tournament Results Database
**Project Description** (from Udacity):
>In this project, you’ll be writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
>You will develop a database schema to store the game matches between players. You will then write a Python module to rank the players and pair them up in matches in a tournament.

### Usage
#### Environment Set up
Make sure you have Git installed. If not, download [here](https://git-scm.com/downloads) <br>
Download and install the correct version of [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) for your operating system <br>
Fork this [directory](ttps://github.com/udacity/fullstack-nanodegree-vm) and copy the newly forked repository path with clone <br>
From terminal:
```
bash-3.2$ git clone PASTE_COPIED_REPO_LINK_HERE fullstack
```
Download tournament.py, tournament.sql, tournament_test.py from this repository <br>
Copy these 3 files to the fullstack directory created from the git clone command
#### Run Program
Open terminal and change directory to the cloned fullstack directory:
```
bash-3.2$ cd FULL_PATH_TO_NEWLY_CLONED_DIRECTORY
```
Use the ls command to see 2 files and 1 directory: CODEOWNERS, README.md, vagrant. Change directory to the tournament directory in the vagrant folder:
```
bash-3.2$ ls
CODEOWNERS    README.md     vagrant
bash-3.2$ cd vagrant/tournament
```
Launch virtual machine:
```
bash-3.2$ vagrant up
```
Log in the virtual machine:
```
bash-3.2$ vagrant sh
vagrant@vagrant:~$
```
Create database and exit PostgreSQL:
```
vagrant@vagrant:~$ psql
vagrant=> \i tournament.sql
vagrant=> \q
```
Run python program:
```
vagrant@vagrant:~$ python tournament_test.py
```
