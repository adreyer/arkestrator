from mdc3.settings import *

ADMINS = (
    ('Rev. Johnny Healey', 'rev.null@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mdc3_dev',                      # Or path to database file if using sqlite3.
        'USER': 'mdc3_dev',                      # Not used with sqlite3.
        'PASSWORD': 'g4mm4r4Y',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

