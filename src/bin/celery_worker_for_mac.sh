#!/bin/sh

python_dir=/usr/local/vpython36
celery_prog=${python_dir}/bin/celery
celeryd_multi_prog=${python_dir}/bin/celeryd-multi
queue=celery #默认队列名称， 多个队列用逗号分隔。
w_total_num=5 #worker个数
default_action=show
log_level=debug

curr_dir=$(/bin/pwd)
#cd ..
if [[ ! -z $1 ]];then
    action=$1
else
    action=${default_action}
fi

w_list=''
x=0
while [ $x -lt $w_total_num ]
do
    let x=x+1
    n_w=$(printf "%03d" $x)
    w_list="${w_list} w${n_w}"
done

if [[ ! -z $2 ]];then
    queue=$2
fi
queue_list=( $(echo $queue|tr ',' ' ') )
len=${#queue_list[*]}
i=0
while [ $i -lt $len ]
do
    if [[ $i -eq 0 ]];then
        queue_name=${queue_list[$i]}
    else
        queue_name="${queue_list[$i]}-${queue_name}"
    fi
    let i=i+1
done

echo "${action} [${w_total_num}] workers for queues: [${queue}] ... "

${celery_prog} multi \
            ${action} \
            ${w_list} \
            -A  config \
            --loglevel=${log_level} \
            -Q ${queue} \
            --without-gossip \
            --without-mingle \
            -Ofair \
            --concurrency=4 \
            --logfile="runtime/log/celery_mult_for_queues_${queue_name}.log" \
            -n worker_for_queues_${queue_name} \
            --pidfile="runtime/pid/celery_mult_%n_for_queues_${queue_name}.pid" \
            --statedb="runtime/tmp/celery_mult_%n_for_queues_${queue_name}.state"

# cd ${curr_dir}
