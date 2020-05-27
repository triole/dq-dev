#!/bin/bash

source "${HOME}/.bashrc"

${HOME}/sh/install-wp.sh
${HOME}/sh/install-daiquiri.sh

cd "${DQAPP}" || exit 1

# install custom and fixture app scripts if there
if [ -f "${DQAPP}/install-custom.sh" ]; then
    echo "Running ${DQAPP} custom installation and fixture script..."
    ${DQAPP}/install-custom.sh
fi

maybe_copy "${HOME}/tpl/wsgi.py" "${DQAPP}/config/wsgi.py" "sudo"

# render wordpress config
cat "${HOME}/tpl/wp-config.php" |
    sd "<WORDPRESS_URL>" "${WORDPRESS_URL}" |
    sd "<SITE_URL>" "${SITE_URL}" |
    sd "<HTTP_HOST>" "${HTTP_HOST}" |
    sd "<GLOBAL_PREFIX>" "${GLOBAL_PREFIX}" |
    sd "<WORDPRESS_DB_NAME>" "${WORDPRESS_DB_NAME}" |
    sd "<WORDPRESS_DB_USER>" "${WORDPRESS_DB_USER}" |
    sd "<WORDPRESS_DB_HOST>" "${WORDPRESS_DB_HOST}" |
    sd "<WORDPRESS_DB_PASSWORD>" "${WORDPRESS_DB_PASSWORD}" \
        >"${HOME}/wp/wp-config.php"

dqip="$(get_container_ip)"
sudo /vol/tools/sd "<PLACEHOLDER>" "${dqip}" \
    "/etc/apache2/sites-enabled/vhost1.conf"

cd "${DQAPP}"
if [[ -z "$(ps aux | grep "[g]unicorn")" ]]; then
    gunicorn --bind 0.0.0.0:8000 \
        --log-file=/dev/stdout \
        --access-logfile=/dev/stdout \
        --workers 2 \
        config.wsgi:application -D
fi

sudo mkdir /run/php
sudo /vol/tools/sd "listen =.*" "listen = /run/php/php.sock" \
    "/etc/php/7.3/fpm/pool.d/www.conf"

# sudo /usr/sbin/apache2 -D FOREGROUND
sudo mkdir -p /run/php
sudo /usr/sbin/php-fpm7.3
sudo /vol/tools/caddy run --config ${HOME}/Caddyfile --adapter caddyfile --watch
