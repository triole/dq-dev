#!/bin/bash

url=$(echo "${CELERY_BROKER_URL}" | grep -Po "(?<=@)[a-zA-Z0-9-_]+")
port=$(echo "${CELERY_BROKER_URL}" | grep -Po "(?<=:)[0-9]+")

max_wait=60

function run_workers() {
    echo "Init celery workers ..."
    cd "${DQAPP}"
    echo "Starts default worker"
    python manage.py runworker default &
    echo "Starts query worker"
    python manage.py runworker query &
    echo "Starts download worker"
    python manage.py runworker download &
}

function is_broker_up() {
    netcat -vz -w 3 ${url} ${port} >/dev/stdout 2>&1 | grep -c 'amqp) open'
}

function init_workers() {
    success="false"
    for i in $(seq 1 ${max_wait}); do
        if [[ "$(is_broker_up)" != "0" ]]; then
            success="true"
            run_workers
            break
        fi
        sleep 1
    done
    if [[ "${success}" == "false" ]]; then
        echo "Failed to run celery workers. Broker was not reachable: ${CELERY_BROKER_URL}"
    fi
}

init_workers

echo "... Celery workers have started"
