#!/bin/bash

mkdir -p runtime/pid
mkdir -p runtime/log
mkdir -p runtime/tmp
mkdir -p data/db
mkdir -p data/conf
mkdir -p data/asset
mkdir -p resource

chown -R www.www runtime
chown -R www.www data

echo 'yes'|/usr/local/python36/bin/python3 manage.py collectstatic
