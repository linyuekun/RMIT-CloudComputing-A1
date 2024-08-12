
===============================
### SET UP NEW EC2 INSTANCE ###
===============================

- Command in case the key is too open:
chmod 400 <path to your key>/<your key>.pem

- Command to install Java
sudo add-apt-repository ppa:linuxuprising/java

- Command to view Ubuntu package that can be updated
sudo apt update

- Command to upgrade Ubuntu packages
sudo apt upgrade

- Command to install JDK 17
sudo apt install oracle-java17-installer

- Command to check version of Java
java -version

- Command to set up Java home environment
export JAVA_HOME=/usr/bin/java 
export PATH=$JAVA_HOME/bin:$PATH

- Command to install Python
sudo apt-get install python3.6

- Command to verify the version of Python
python3 --version

- Command to install pip
sudo apt install python3-pip

- Command to verify the version of pip
pip3 --version

- Command to install Apache2
sudo apt-get install apache2

- Command to install PHP
sudo apt-get install php libapache2-mod-php
sudo a2enmod mpm_prefork && sudo a2enmod php7.4
 
- Command to start Apache web server
sudo service apache2 start

- Command to restart Apache web server
sudo service apache2 restart

- Command to set permission of MyServer
sudo chmod -R 777 /var/www/html

- Command to install and interact with nginx
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl stop nginx
sudo systemctl status nginx

- Command to set a new config file for reverse proxy:
sudo nano /etc/nginx/sites-enabled/<your config file>


- Reverse proxy config to be edited
server {
    listen 80;
    listen [::]:80;
    server_name <Public IPv4 DNS for EC2 Instance>;
        
    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }
}

- Create Directories
mkdir ~/templates
mkdir ~/.aws

- Exit instance and paste the following files

scp -i <path to your key>/<your key>.pem ~/.aws/config ubuntu@<Public IPv4 DNS for EC2 Instance>:~/.aws/config

scp -i <path to your key>/<your key>.pem ~/.aws/credentials ubuntu@<Public IPv4 DNS for EC2 Instance>:~/.aws/credentials

scp -i <path to your key>/<your key>.pem <path to your file>/requirements.txt ubuntu@<Public IPv4 DNS for EC2 Instance>:~/requirements.txt

- Go back to EC2 instance
ssh -i <path to your key>/<your key>.pem ubuntu@<Public IPv4 DNS for EC2 Instance>

- Command to install all packages needed for running Flask app
pip install -r requirements.txt

============
### RUN ###
============

- Command to access EC2 Instance:
ssh -i <path to your key>/<your key>.pem ubuntu@<Public IPv4 DNS for EC2 Instance>

- Command to edit credentials
nano ~/.aws/credentials

- Credentials to be edited
[default]
aws_access_key_id=<aws_access_key_id>
aws_secret_access_key=<aws_secret_access_key>
aws_session_token=<aws_session_token>

- Command to change DNS for reversed proxy
sudo nano /etc/nginx/sites-enabled/<your config file>

- Reverse proxy config to be edited
server {
    listen 80;
    listen [::]:80;
    server_name <Public IPv4 DNS for EC2 Instance>;
        
    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }
}

- Command to check if the port is used
sudo lsof -i :80
sudo lsof -i :5000

- Command to run app
python3 app.py

- Command to check nginx
sudo systemctl restart nginx
sudo systemctl status nginx

- Command to terminate
sudo systemctl stop nginx
sudo systemctl stop apache2

===============
### UPDATE ###
===============

scp -i <path to your key>/<your key>.pem <path to your file>/app.py ubuntu@<Public IPv4 DNS for EC2 Instance>:~/app.py

scp -i <path to your key>/<your key>.pem <path to your file>/app.py ubuntu@<Public IPv4 DNS for EC2 Instance>:~/templates/main.html

scp -i <path to your key>/<your key>.pem <path to your file>/app.py ubuntu@<Public IPv4 DNS for EC2 Instance>:~/templates/register.html

scp -i <path to your key>/<your key>.pem <path to your file>/app.py ubuntu@<Public IPv4 DNS for EC2 Instance>:~/templates/login.html

