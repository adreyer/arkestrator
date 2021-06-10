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
        'ply==3.11',
        'django==2.2.24',
        'python-memcached==1.59',
        'pytz==2014.7',
        'psycopg2-binary==2.8.5',
      ],
    )
