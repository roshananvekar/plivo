
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm




def deploy():
    run("sudo apt-get update")
    run("sudo apt-get install python-pip")
    #run("sudo pip install virtualenv")
    #run("virtualenv uwsgi-tutorial")
    #run("source uwsgi-tutorial/bin/activate")
    #cd("/home/ubuntu/uwsgi-tutorial")
    run("pip install Django")
    run("/usr/local/bin/django-admin.py startproject mysite")
    #cd("/home/ubuntu//mysite")
    run("pip install uwsgi")
    #run("python mysite/manage.py runserver 0.0.0.0:8000")
    
