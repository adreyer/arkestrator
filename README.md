Local development installation
==============================

System setup
------------

To hack on Arkestrator, you will need some basic components installed on your system:

- A recent Python (we recommend 2.7)
- Virtualenv
- Pip
- A relational database supported by Django

On a Debian Wheezy system, for example, you should be able to get these things by running:

```bash
apt-get install python2.7 python-pip python-virtualenv python-dev
```

You will also need a database. SQLite 3 might still work, so perhaps you can get away with:

```bash
apt-get install sqlite3
```

We all use PostgreSQL because it is awesome. If you want to use PostgreSQL, in addition to the server and the client libraries, you'll need the development headers so that you can build Pyscopg2 inside your virtualenv later on:

```bash
apt-get install postgresql postgresql-server-dev-9.1
```

At this point, you should have all of the prerequisites for building a local Arkestrator environment.

Virtualenv setup
----------------

On Github, you should fork the main Arkestrator repository. Visit https://github.com/adreyer/arkestrator and click the "fork" button. If you want to work on BBKing, you should visit https://github.com/adreyer/BBKing and fork that too.

Next, create a virtualenv and activate it.

```bash
cd ~/virtualenvs
virtualenv ark
cd ark
source bin/activate
```

We are going to install Arkestrator using Pip. We are using `pip -e` so that these repositories are editable. **Substitute your own fork's URL here.** You'll want to add adreyer's repo as your upstream remote, too:

```bash
pip install -e git+ssh://git@github.com/cmroddy/arkestrator.git#egg=mdc3
cd ~/virtualenvs/ark/src/mdc3/
git remote add upstream https://github.com/adreyer/arkestrator.git
```

If you want to work on BBKing, install that the same way:

```bash
pip install -e git+ssh://git@github.com/cmroddy/BBKing.git#egg=bbking
cd ~/virtualenvs/ark/src/bbking
git remote add upstream https://github.com/adreyer/BBKing.git
```

If you don't want to work on BBKing, you can just install it with the rest of the requirements. Regardless, you need to install them, so:

```bash
cd $path_to_arkestrator_clone
pip install -r requirements.txt
```

At this point, you should have all the Python code you need. Maybe Psycopg2 failed to build or something else failed to install, so make sure there are no errors in the output from Pip. If there are, fix the problem and try again.

Sync and migrate database
-------------------------

You will need to sync and migrate your database. If you're using SQLite, make sure that you keep track of where the local database file is. Your working directory actually matters. If you're using Postgres, make sure that you've created an appropriate user and database. You probably need to edit `pg_hba.conf`. Whatever, I am not going to tell you how to administer your database server.

To sync and migrate the database, run:

```bash
django-admin.py syncdb --migrate --settings=mdc3.settings
```

This should spew out a bunch of output about table creation, prompt you to create an admin account, and then spew out a bunch more output about schema migrations. If there are any problems, fix them.

Run the development server
--------------------------

If you made it this far, then everything should be working. Start the development server:

```bash
django-admin.py runserver --settings=mdc3.settings
```


Production installation
=======================

Production installation is possible.
