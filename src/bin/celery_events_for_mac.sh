#!/bin/sh

curr_dir=$(/bin/pwd)
#cd ..
python_dir=/usr/local/vpython36
celery_prog=${python_dir}/bin/celery
${celery_prog} -A  config  -Q

#cd ${curr_dir}
