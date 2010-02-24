
from distutils.code import setup

setup(name="mdc3",
    version="0.0.1",
    description="An Internet Message Board",
    author="Rev. Johnny Healey",
    author_email="rev.null@gmail.com",
    packages=[
        'mdc3',
        'mdc3.board',
        'mdc3.gallery',
        'mdc3.invites',
        'mdc3.profiles',
        'mdc3.shenanigans',
        'mdc3.tags',
        'mdc3.themes'
    ],
    package_data={
        'mdc3':['media/*','templates/*'],
        'mdc3.board':['templates/*']
    })

