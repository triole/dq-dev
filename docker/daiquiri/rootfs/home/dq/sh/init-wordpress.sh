#!/bin/bash

wp core install \
    --path=${WORDPRESS_PATH} \
    --url="http://localhost:${EXPOSED_PORT}${WORDPRESS_URL}" \
    --title="${WORDPRESS_TITLE}" \
    --admin_user=dqadmin \
    --admin_email=admin@dqdev.de \
    --admin_password=14rets6dyfufhgji789 \
    --skip-email

wp plugin activate --path=${WORDPRESS_PATH} daiquiri
wp theme activate --path=${WORDPRESS_PATH} daiquiri
