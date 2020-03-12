#!/bin/sh

curr_dir=$(/bin/pwd)
#cd ..
w_num=$1
python_dir=/usr/local/vpython36
celery_prog=${python_dir}/bin/celery
#${celery_prog} -A  config   flower --port=5555  -l  debug --uid=spunkmars --gid=staff  --persistent=True --db=data/db/flower
${celery_prog} -A  config   flower --port=5555 --persistent=True  --db=data/db/flower.db -l  debug

#cd ${curr_dir}
