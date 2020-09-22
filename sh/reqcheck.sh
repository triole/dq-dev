#!/bin/bash
# simple request check script to test reverse proxy redirects

function req() {
    cmd="curl -sL http://localhost:9280${1}"
    if (($(curl -sL http://localhost:9280${1} | grep -ci "${2}") > 0)); then
        printf "\033[0;32m[good]\033[0m "
    else
        printf "\033[0;31m[fail]\033[0m "
    fi
    echo ${cmd}
}

# main
req "" "A framework for the publication of scientific databases"
req / "A framework for the publication of scientific databases"

req /cms "Welcome to WordPress. This is your first post."
req /cms/ "Welcome to WordPress. This is your first post."

req /cms/admin "If you have not created an account yet"
req /cms/admin/ "If you have not created an account yet"

req /cms/wp-admin "If you have not created an account yet"
req /cms/wp-admin/ "If you have not created an account yet"
