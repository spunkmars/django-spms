#!/bin/sh

curr_dir=$(/bin/pwd)
#cd ..
action=$1

nohup /bin/bash bin/celery_flow_for_mac.sh &
nohup  /bin/bash bin/celery_worker_for_mac.sh start celery &
nohup /bin/bash bin/celery_beat_for_mac.sh &
nohup daphne -b 0.0.0.0 -p 8008 config.asgi:application & # channels asgi
echo
