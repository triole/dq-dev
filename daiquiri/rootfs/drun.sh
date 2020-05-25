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

# sudo mkdir -p "/etc/httpd/vhosts.d"
# maybe_copy "/tmp/vhost2.conf" "/etc/httpd/vhosts.d/vhost2.conf" "sudo"
maybe_copy "/tmp/wsgi.py" "${DQAPP}/config/wsgi.py" "sudo"

replace_ip_in_vhost

cd "${DQAPP}"
if [[ -z "$(ps aux | grep "[g]unicorn")" ]]; then
    gunicorn --bind 0.0.0.0:8000 \
        --log-file=/dev/stdout \
        --access-logfile=/dev/stdout \
        --workers 2 \
        config.wsgi:application -D
fi

sudo a2enmod proxy
sudo a2enmod rewrite
sudo /usr/sbin/apache2 -D FOREGROUND
