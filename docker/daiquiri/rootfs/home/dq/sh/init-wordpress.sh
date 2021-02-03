#!/bin/bash

USER="${WORDPRESS_ADMIN_USER}"
PASS="${WORDPRESS_ADMIN_PASSWORD}"
MAIL="${WORDPRESS_ADMIN_EMAIL}"

echo "Init wordpress"

wp core install \
    --path="${WORDPRESS_PATH}" \
    --url="http://localhost:${EXPOSED_PORT}${WORDPRESS_URL}" \
    --title="${WORDPRESS_TITLE}" \
    --admin_user=admin \
    --admin_email=admin@dqdev.de \
    --admin_password=admin \
    --skip-email

uid=$(
    wp user create "${USER}" "${MAIL}" \
        --path="${WORDPRESS_PATH}" \
        --user_pass="${PASS}" \
        --role=administrator \
        --porcelain
)

wp user delete 1 --reassign=${uid} --path="${WORDPRESS_PATH}" --yes

wp plugin activate --path=${WORDPRESS_PATH} daiquiri
wp theme activate --path=${WORDPRESS_PATH} daiquiri
