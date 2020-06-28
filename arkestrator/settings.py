# Django settings for arkestrator project.
import os

DEBUG = True

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'arkestrator',                      # Or path to database file if using sqlite3.
        'USER': 'arkestrator',                      # Not used with sqlite3.
        'PASSWORD': 'hello12',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'dummy://'
#CACHE_BACKEND = "memcached://127.0.0.1:11211/"
#CACHE_MIDDLEWARE_KEY_PREFIX="MDC3DEV"

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "%s/media"%BASE_DIR

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_ROOT = "%s/static" % BASE_DIR 
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c8-s2vc_*&(c(^!se3m3gi-lu)i+uod*!qb*ld^%06*a40443('

TEMPLATES = [
        { 'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'APP_DIRS': True,
          'DIRS': [
              "%s/templates" % BASE_DIR,
          ],
          'OPTIONS': {
              'debug': DEBUG,
              'context_processors': [
                  'django.contrib.auth.context_processors.auth',
                  'django.template.context_processors.debug',
                  'django.template.context_processors.i18n',
                  'django.template.context_processors.media',
                  'django.contrib.messages.context_processors.messages',
                  'arkestrator.context_processors.site_name',
                  'arkestrator.pms.context_processors.new_pm',
                  'arkestrator.context_processors.online_users',
                  'arkestrator.board.context_processors.thread_count',
                  'arkestrator.board.context_processors.posting_users',
                  'arkestrator.invites.context_processors.new_invites',
                  'arkestrator.events.context_processors.new_events',
              ]}},
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'arkestrator.moderation.middleware.BanMiddleware',
    'arkestrator.middleware.OnlineUsersMiddleware',
    'arkestrator.board.middleware.PostingUsersMiddleware',
)

ROOT_URLCONF = 'arkestrator.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'bbking',
    'oembed',
    'arkestrator.board',
    'arkestrator.themes',
    'arkestrator.profiles',
    'arkestrator.invites',
    'arkestrator.pms',
    'arkestrator.util',
    'arkestrator.shenanigans',
    'arkestrator.events',
    'arkestrator.moderation',
)

AUTH_PROFILE_MODULE = 'profiles.Profile'
LOGIN_REDIRECT_URL = '/'

##  the choices for profile.time_zone which determines what time zones
##  are available to users
TZ_CHOICES = (('America/New_York'    , 'America/New_York'),
              ('America/Chicago'     , 'America/Chicago'),
              ('America/Denver'      , 'America/Denver'),
              ('America/Los_Angeles' , 'America/Los_Angeles'),
            )
##  the default timezone when profiles.time_zone isn't set
DEFAULT_TZ = 'America/New_York'

## the default time format to use from TIME_FORMATS
DEFAULT_TIME_FORMAT = 'long'

##  the time format options available for mdc_time
TIME_FORMATS = { 'short'    : '%I:%M %p %d-%b-%y',
                 'long'     : '%a, %d-%b-%Y at %I:%M:%S %p',
                 'date'     : '%d-%b-%Y',}

BBKING_TAG_LIBRARIES = (
                        'bbking.bbtags.text',
                        'bbking.bbtags.hrefs',
                        'bbking.bbtags.quote',
                        'bbking.bbtags.code',
                        'bbking.bbtags.embed',
                        'arkestrator.bbtags',
                    )

BBKING_USE_WORDFILTERS = True

PARSER_DIR='/home/rev/src/arkestrator'

OEMBED_MAX_WIDTH = 640
OEMBED_MAX_HEIGHT = 640

EMAIL_FROM = 'arkestrator@example.com'
