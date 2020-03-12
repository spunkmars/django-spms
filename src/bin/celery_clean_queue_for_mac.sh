#!/bin/sh

python_dir=/usr/local/vpython36
celery_prog=${python_dir}/bin/celery
if [[ ! -z $1 ]];then
    queue=$1
else
    queue=celery
fi
curr_dir=$(/bin/pwd)
#cd ..

echo "Clean queues: ${queue} ..."
${celery_prog} purge -A  config  -Q${queue} -f

#cd ${curr_dir}
