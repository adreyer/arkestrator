# Django settings for mdc3 project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'local.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'dummy://'

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

# TODO: should these be the same?
STATIC_ROOT = MEDIA_ROOT
STATIC_URL = MEDIA_URL

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c8-s2vc_*&(c(^!se3m3gi-lu)i+uod*!qb*ld^%06*a40443('

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'mdc3.moderation.middleware.BanMiddleware',
    'mdc3.middleware.OnlineUsersMiddleware',
    'mdc3.board.middleware.PostingUsersMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "mdc3.context_processors.site_name",
    "mdc3.pms.context_processors.new_pm",
    "mdc3.context_processors.online_users",
    "mdc3.board.context_processors.thread_count",
    "mdc3.board.context_processors.posting_users",
    "mdc3.invites.context_processors.new_invites",
    "mdc3.events.context_processors.new_events",
)

ROOT_URLCONF = 'mdc3.urls'

TEMPLATE_DIRS = (
    "%s/templates"%BASE_DIR,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'mdc3.board',
    'mdc3.themes',
    'mdc3.profiles',
    'mdc3.invites',
    'mdc3.pms',
    'mdc3.util',
    'mdc3.shenanigans',
    'mdc3.events',
    'mdc3.moderation',
    'oembed',
    'bbking',
    'haystack',
    'debug_toolbar',
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
                        'mdc3.bbtags',
                    )

BBKING_USE_WORDFILTERS = True

HAYSTACK_SITECONF = 'mdc3.search_sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

OEMBED_MAX_WIDTH = 640
OEMBED_MAX_HEIGHT = 640


# DDTB settings
# too lazy to put this anywhere else
def custom_show_toolbar(request):
  return request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
}
