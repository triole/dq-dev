#!/bin/bash

source "${HOME}/.bashrc"

${HOME}/sh/install-daiquiri.sh

cd "${DQAPP}" || exit 1

# install custom and fixture app scripts if there
if [ -f "${DQAPP}/install-custom.sh" ]; then
    echo "Running ${DQAPP} custom installation and fixture script..."
    ${DQAPP}/install-custom.sh
fi

sfil="${HOME}/tpl/wsgi.py"
tfil="${DQAPP}/config/wsgi.py"
if [[ ! -f "${tfil}" ]]; then
    copy -f "${sfil}" "${tfil}"
fi

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

${HOME}/sh/init-wordpress.sh

cd "${DQAPP}"
if [[ -z "$(ps aux | grep "[g]unicorn")" ]]; then
    # django dev server for development, has auto reload, does no cache
    python3 manage.py runserver 0.0.0.0:8000 &

    # gunicorn --bind 0.0.0.0:8000 \
    #     --log-file=/dev/stdout \
    #     --access-logfile=/dev/stdout \
    #     --workers 2 \
    #     config.wsgi:application -D
fi

sudo /usr/sbin/php-fpm7.3
sudo /vol/tools/shed/caddy run --config ${HOME}/Caddyfile --adapter caddyfile --watch
