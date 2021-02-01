#!/bin/bash

wp core install \
    --path=${WORDPRESS_PATH} \
    --url="http://localhost:${EXPOSED_PORT}${WORDPRESS_URL}" \
    --title="${WORDPRESS_TITLE}" \
    --admin_user=dqadmin \
    --admin_email=dqadmin@sirrah.de \
    --admin_password=4fb4cb000853f6cc7a6012202d2af4e3 \
    --skip-email

wp plugin activate --path=${WORDPRESS_PATH} daiquiri
wp theme activate --path=${WORDPRESS_PATH} daiquiri
