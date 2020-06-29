Local development installation
==============================

System setup
------------

To hack on Arkestrator, you will need some basic components installed on your system:

- Python 3.7+
- Virtualenv
- Pip
- Postgresql 9+

On a Debian system, for example, you should be able to get these things by running:

```bash
apt-get install python3 python3-pip python3-virtualenv python3-dev
```

At this point, you should have all of the prerequisites for building a local Arkestrator environment.

Virtualenv setup
----------------

On Github, you should fork the main Arkestrator repository.

Next, create a virtualenv and activate it.

```bash
cd ~/virtualenvs
python3 -mvenv ark
cd ark
source bin/activate
```

We are going to install Arkestrator using Pip. We are using `pip -e` so that these repositories are editable. **Substitute your own fork's URL here.** You'll want to add adreyer's repo as your upstream remote, too:

```bash
pip install -e git+ssh://git@github.com/cmroddy/arkestrator.git#egg=arkestrator
cd ~/virtualenvs/ark/src/arkestrator/
git remote add upstream https://github.com/adreyer/arkestrator.git
```

At this point, you should have all the Python code you need.

Sync and migrate database
-------------------------

You will need to sync and migrate your database. You may need to edit `pg_hba.conf`. Whatever, I am not going to tell you how to administer your database server.

To use the provided dev settings create the following user and database in postgres:

```sql
CREATE USER arkestrator_dev WITH PASSWORD 'g4mm4r4y';
CREATE DATABASE arkestrator_dev WITH OWNER arkestrator_dev;
```

To sync and migrate the database, run:

```bash
./manage.py migrate --settings=arkestrator.settings
```

This should spew out a bunch of output about table creation, prompt you to create an admin account, and then spew out a bunch more output about schema migrations. If there are any problems, fix them.

Run the development server
--------------------------

If you made it this far, then everything should be working. Start the development server:

```bash
./manage.py runserver --settings=arkestrator.settings
```


Production installation
=======================

Production installation is possible.
