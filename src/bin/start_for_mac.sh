#!/bin/bash

user='spunkmars'
group='staff'
python_path='/usr/local/vpython36/'
uwsgi_prog=${python_path}/bin/uwsgi
gunicorn_prog=${python_path}/bin/gunicorn
proj_path='/Users/spunkmars/SM-H/django-spms/src'
cd ${proj_path}
#mkdir -p data/db
#mkdir -p data/asset
#chown -R ${user}.${group} data

#nohup redis-server >/dev/null 2>&1  &


export DJANGO_ENV='prod'
#${uwsgi_prog} --ini ${proj_path}/data/uwsgi/uwsgi_httpsocket_for_mac_9091.ini
${gunicorn_prog} -c ${proj_path}/data/gunicorn/gunicorn.conf -e DJANGO_ENV=${DJANGO_ENV}  config.wsgi
