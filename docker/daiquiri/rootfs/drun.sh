#!/bin/bash

source "${HOME}/.bashrc"

${HOME}/sh/install-caddy.sh
${HOME}/sh/install-daiquiri.sh

cd "${DQAPP}" || exit 1

sfil="${HOME}/tpl/wsgi.py"
tfil="${DQAPP}/config/wsgi.py"
if [[ ! -f "${tfil}" ]]; then
    copy -f "${sfil}" "${tfil}"
fi

# render config files
${HOME}/sh/expand-env-vars.sh \
    "${HOME}/tpl/wp-config.php" "${WORDPRESS_PATH}/wp-config.php"

${HOME}/sh/expand-env-vars.sh \
    "${HOME}/tpl/Caddyfile.tpl" "${HOME}/Caddyfile"

${HOME}/sh/init-wordpress.sh
${HOME}/sh/init-folders.sh

# install custom and fixture app scripts if there
if [ -f "${DQAPP}/install-custom.sh" ]; then
    echo "Run ${DQAPP} custom installation and fixture script..."
    ${DQAPP}/install-custom.sh
fi

cd "${DQAPP}"
if [[ -z "$(ps aux | grep "[g]unicorn")" ]]; then
    # django dev server for development, has auto reload, does not cache
    python3 manage.py runserver 0.0.0.0:8000 &

    # gunicorn --bind 0.0.0.0:8000 \
    #     --log-file=/dev/stdout \
    #     --access-logfile=/dev/stdout \
    #     --workers 2 \
    #     config.wsgi:application -D
fi

if [[ "${ASYNC}" == "True" ]]; then
    ${HOME}/sh/init-rabbitmq-workers.sh &
fi

/usr/sbin/php-fpm7.3
caddy run --config ${HOME}/Caddyfile --adapter caddyfile --watch
