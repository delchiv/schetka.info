## Requird nonroot user account with sudo privilegies

    sudo useradd -m -s /bin/bash USERNAME
    sudo usermod -a -G sudo USERNAME
    sudo passwd USERNAME
    sudo su - USERNAME

## Nginx password access to server

    sudo apt-get install apache2-utils
    sudo htpasswd -c /etc/nginx/.htpasswd exampleuser

## Required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf

* replace SITENAME with, eg, staging.my-domain.com
* replace USERNAME with actual user

* uncomment if you need password access to server
*   auth_basic "Restricted";
*   auth_basic_user_file /etc/nginx/.htpasswd;

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
