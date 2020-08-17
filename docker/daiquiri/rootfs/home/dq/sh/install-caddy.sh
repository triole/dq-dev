#!/bin/bash

function install_caddy() {
    tmpfil="/tmp/caddy.tar.gz"
    tfol="${HOME}/bin"

    echo "Did not find caddy on volume. Download binary from ${CADDY_BIN_URL}"

    caddy_bin_url="https://github.com/$(
        curl -Ls "https://github.com/caddyserver/caddy/releases/latest" |
            grep -Po "(?<=href\=\").*linux_amd64\.tar.gz?(?=\")"
    )"

    mkdir -p "${tfol}"
    curl -Ls ${caddy_bin_url} -o "${tmpfil}" &&
        tar xf "${tmpfil}" -C "${tfol}"

    sudo rm -f "/bin/caddy"
    sudo ln -s "${HOME}/bin/caddy" "/bin/caddy"

    echo "Caddy version $(caddy version) installed"
}

sudo caddy version || install_caddy
