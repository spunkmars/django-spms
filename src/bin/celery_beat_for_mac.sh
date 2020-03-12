#!/bin/sh

curr_dir=$(/bin/pwd)
#cd ..
action=$1
python_dir=/usr/local/vpython36
celery_prog=${python_dir}/bin/celery
pid_file=runtime/pid/celery_beat.pid
log_file=runtime/log/celery_beat.log
[[ -f ${log_file} ]] && rm -f ${log_file}
[[ -f ${pid_file} ]] && rm -r ${pid_file}

#${celery_prog} beat  -A config --logfile=${log_file} --loglevel=debug --pidfile=${pid_file}
${celery_prog} beat  -A config --scheduler=django_celery_beat.schedulers:DatabaseScheduler --schedule='data/db/celerybeat-schedule.db' --logfile=${log_file} --loglevel=debug --pidfile=${pid_file}
#${celery_prog} beat  -A config  --schedule='data/db/celerybeat-schedule.db'  --logfile=${log_file} --loglevel=debug --pidfile=${pid_file}
# --scheduler django_celery_beat.schedulers:DatabaseScheduler # 使用插件django_celery_beat
#--workdir=./
#--detach # 后台执行
# --schedule='data/db/celerybeat-schedule.db'

# cd ${curr_dir}
