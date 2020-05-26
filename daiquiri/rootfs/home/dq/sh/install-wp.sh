#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${scriptdir}/source.sh"

# install wordpress
cd "/tmp"
if [[ ! -f "${WP}/wp-config.php" ]]; then
    echo "install wordpress"
    curl -O https://wordpress.org/latest.tar.gz
    mkdir -p "${WP}"
    tar xzvf latest.tar.gz -C "${WP}" --strip-components=1

    echo "install wordpress cli"
    curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
    sudo chmod +x wp-cli.phar
    sudo mv wp-cli.phar /usr/bin/wp
fi

# wordpress config setup
conf="${WP}/wp-config.php"
maybe_copy "/tmp/wp-config-tpl.php" "${conf}"
sd "DAIQUIRI_URL" "http://localhost:80" "${conf}"
sd "WP_HOME" "http://localhost:9280/cms" "${conf}"
sd "WP_SITEURL" "http://localhost:9280/cms" "${conf}"

# daiquiri theme and plugin
clone https://github.com/django-daiquiri/wordpress-plugin ${WP}/wp-content/plugins/daiquiri
clone https://github.com/django-daiquiri/wordpress-theme ${WP}/wp-content/themes/daiquiri
sudo chown -R ${USER}:apache "${WP}"
sudo chmod -R u=rwx,g=rwx "${WP}"
