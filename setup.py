from setuptools import setup, find_packages

setup(
    name="arkestrator",
    version="0.0.1",
    description="An Internet Message Board",
    author="Rev. Johnny Healey",
    author_email="rev.null@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
	'bbking==0.0.1',
        'django==1.6.11',
        'south==0.7.3',
        'python-memcached==1.48',
        'pytz==2014.7',
        'django-haystack==1.2.7',
        'simplejson==2.3.0',
        'psycopg2-binary==2.8.3',
        'pysolr==2.1.0-beta',
        'multiprocessing==2.6.2.1',
        'BeautifulSoup==3.2.0',
        'unittest2==0.5.1',
        'mock==0.7.2',
        'django-oembed==0.1.3',
        'django-debug-toolbar==0.11.0',
      ],
    )
