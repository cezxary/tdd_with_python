Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.8
* virtualenv + pip
* Git

eg. on Ubuntu 20.04:

	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install nginx git python38 python3.8-venv

eg. at small.pl:

	python already installed
	git already installed

## Adding new domain

	run 'devil www add DOMAIN python PYTHON_VENV_BINARY_LOCATION staging' to add a new domain using python

## Phusion Passenger config:

* see passenger\_wsgi.py
* copy that file to BASE\_DIR
* replace PROJECT with main settings project
* perform python manage.py collectstatic to get static files in directory static/
* move directory static/ into directory public/

## Folder structure:

Assume we have a user account at /home/username

/home/username/domains
├── DOMAIN1
│   └── public\_python
│       ├── .env.json
│       ├── passenger\_wsgi.py
│       ├── db.sqlite3
│       ├── manage.py etc
│       └── public
│           └── static
└── DOMAIN2
   └── public\_python
	    ├── .env.json
	    ├── db.sqlite3
	    └── etc


