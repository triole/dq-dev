#!/bin/bash

# adapted from: https://stackoverflow.com/a/52309688 (CC-BY-SA 4.0)

# This script needs to be executed just once
if [ -f /$0.completed ] ; then
  echo "$0 `date` /$0.completed found, skipping run"
  exit 0
fi

# Wait for RabbitMQ startup
for (( ; ; )) ; do
  sleep 5
  rabbitmqctl -q node_health_check > /dev/null 2>&1
  if [ $? -eq 0 ] ; then
    echo "$0 `date` rabbitmq is now running"
    break
  else
    echo "$0 `date` waiting for rabbitmq startup"
  fi
done

# Execute RabbitMQ config commands here

# set user, vhost and permissions
rabbitmqctl add_user ${RABBITMQ_USER} ${RABBITMQ_PASSWORD}
rabbitmqctl add_vhost ${RABBITMQ_VHOST}
rabbitmqctl set_permissions -p ${RABBITMQ_VHOST} ${RABBITMQ_USER} ".*" ".*" ".*"
rabbitmqctl set_permissions -p ${RABBITMQ_VHOST} ${RABBITMQ_DEFAULT_USER} ".*" ".*" ".*"

echo "$0 `date` user ${RABBITMQ_USER} created"

# Create mark so script is not ran again
touch /$0.completed
