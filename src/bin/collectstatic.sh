#!/bin/bash

curr_path=$(pwd)
#cd /data/htdocs/www/django-spms/src
cd /Users/spunkmars/SM-H/django-spms/src

#echo 'yes'|/usr/local/python36/bin/python3 manage.py collectstatic
/usr/local/vpython36/bin/python3 manage.py collectstatic --noinput

# 修改权限，使得打包时候非root用户挂载目录可修改此目录属主
if [[ ! -z ${DOCKER_CONTAINER} && ${DOCKER_CONTAINER} == 1 ]];then
    chmod -R 777 /data/htdocs/www/django-spms/resource
fi

cd ${curr_path}