from fabric.api import run, env
import datetime

env.hosts = ['mdc2.org']
env.user = 'deploy'

remote_dir = '/var/mdc3'
repo = '/var/cache/hg/repos/mdc3'

def deploy():
    ts = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    release_dir = "%s/releases/%s"%(remote_dir,ts)
    current_dir = "%s/current" % remote_dir

    # clone the repo
    run("hg clone %s %s"%(repo,release_dir))

    # change the symlink for the current release
    run("ln -fsT %s %s"%(release_dir,current_dir))

    # remove all but the last 5 releases
    run("cd %s/releases; rm -fr `ls -t | awk 'NR>5'`"%remote_dir)

