from fabric.api import run, env, sudo
import datetime

env.hosts = ['mdc2.org']
env.user = 'deploy'

# this values should be project specific
remote_dir = '/var/mdc3'
repo = '/var/cache/hg/repos/mdc3'
settings_module = "mdc3.settings_dev"

#these should be computed based on the project specific settings
releases_dir = "%s/releases"%remote_dir
current_dir = "%s/current" % remote_dir
package_dir = "%s/packages"%remote_dir

def deploy():
    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    release_dir = "%s/%s"%(releases_dir,ts)

    # clone the repo
    run("hg clone %s %s"%(repo,release_dir))

    # change the symlink for the current release
    run("ln -fsT %s %s"%(release_dir,current_dir))

    # remove all but the last 5 releases
    run("cd %s/releases; rm -fr `ls -t | awk 'NR>5'`"%remote_dir)

    # graceful the web servers
    run("sudo /etc/init.d/julep graceful")
    run("sudo /etc/init.d/apache2 reload")

def rollback():
    run("cd %s; ln -fsT `ls -t | awk 'NR>1'| head -n 1` %s"%
        (releases_dir,current_dir))

    run("cd %s; rm -fr `ls -t | head -n 1`"%releases_dir)

    # graceful the web servers
    run("sudo /etc/init.d/julep graceful")
    run("sudo /etc/init.d/apache2 reload")

def list_releases():
    run("ls -t %s"%releases_dir)

def syncdb():
    run("export PYTHONPATH=%s; django-admin.py syncdb --settings=%s"%
        (package_dir,settings_module))

