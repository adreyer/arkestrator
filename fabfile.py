# "I am from the future!" -Sayid Jarrah
from __future__ import with_statement

from fabric.api import run, env, sudo, require, cd
import datetime

env.hosts = ['mdc2.org']
env.user = 'deploy'

def dev():
    "The Development Environment"
    env.remote_dir = '/var/mdc3_dev'
    env.repo = '/var/cache/hg/repos/mdc3'
    env.settings_module = "mdc3.settings_dev"
    _set_extra_dirs()

def prod():
    "The Production Environment"
    env.remote_dir = '/var/mdc3'
    env.repo = '/var/cache/hg/repos/mdc3'
    env.settings_module = "mdc3.settings_prod"
    _set_extra_dirs()

def _set_extra_dirs():
    require('remote_dir',
        provided_by=['dev','prod'])

    env.releases_dir = "%(remote_dir)s/releases"%env
    env.current_symlink = "%(remote_dir)s/current"%env
    env.package_dir = "%(remote_dir)s/packages"%env
    env.virtualenv = "%(remote_dir)s/virtualenv"%env

def rebuild_virtualenv():
    with cd("%(remote_dir)s"%env):
        run("rm -fr %(virtualenv)s"%env)
        run("virtualenv %(virtualenv)s"%env)
        run("""
        source %(virtualenv)s/bin/activate;
        pip install -r %(current_symlink)s/requirements.txt
        """%env)
    
def graceful_servers():
    "Gracefully restart the web servers"
    # graceful the web servers
    sudo("/etc/init.d/julep graceful",shell=False)
    sudo("/etc/init.d/apache2 reload",shell=False)

def deploy():
    "Deploy the code and gracefully restart the web servers"

    require('releases_dir','repo','current_symlink',
        provided_by=['dev','prod'])

    # the release dir is named after the timestamp
    env.ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    env.release_dir = "%(releases_dir)s/%(ts)s"%env

    # clone the repo
    run("hg clone %(repo)s %(release_dir)s"%env)

    # change the symlink for the current release
    run("ln -fsT %(release_dir)s %(current_symlink)s"%env)

    cleanup()
    graceful_servers()

def rollback():
    "Roll back the code to the previous released version"

    require('releases_dir','current_symlink',
        provided_by=['dev','prod'])

    with cd("%(releases_dir)s"%env):
        # change symlink to previous release
        run("ln -fsT `ls -t | awk 'NR>1'| head -n 1` %(current_symlink)s"%env)

        # remove latest release
        run("rm -fr `ls -t | head -n 1`")

    graceful_servers()

def list_releases():
    "List the releases on the server"

    require('releases_dir',
        provided_by=['dev','prod'])

    run("ls -t %(releases_dir)s"%env)

def syncdb():
    "Run the django syncdb process"
    require('settings_module','package_dir',
        provided_by=['dev','prod'])

    run("""
    source %(virtualenv)s/bin/activate;
    django-admin.py syncdb --no-input --settings=%(settings_module)s \
        --pythonpath=%(current_symlink)s
    django-admin.py migrate --settings=%(settings_module)s \
        --pythonpath=%(current_symlink)s
    """%env)

def cleanup():
    "Remove all but the 5 most recent releases"
    require('releases_dir',
        provided_by=['dev','prod'])

    # remove all but the last 5 releases
    with cd("%(releases_dir)s"%env):
        run("rm -fr `ls -t | awk 'NR>5'`")

