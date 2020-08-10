#!/bin/bash

wp core install \
    --path=${WORDPRESS_PATH} \
    --url="http://localhost:9280/cms" \
    --title="dqdev" \
    --admin_user=admin \
    --admin_email=admin@dqdev.de \
    --admin_password=admin \
    --skip-email
