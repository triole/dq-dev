#!/bin/bash

url=$(echo "${CELERY_BROKER_URL}" | grep -Po "(?<=@)[a-zA-Z0-9-_]+")
port=$(echo "${CELERY_BROKER_URL}" | grep -Po "(?<=:)[0-9]+")

max_wait=60

function run_workers() {
    echo "Init rabbitmq workers"
    cd "${DQAPP}"
    python manage.py runworker default
    python manage.py runworker query
    python manage.py runworker download
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
