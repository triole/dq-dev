#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${scriptdir}/source.sh"

if [[ $(pip3 freeze | grep -Poc "django-daiquiri") == "0" ]]; then

    cd "${DQSOURCE}" || exit 1
    pip3 install -e "${DQSOURCE}"

    cd "${DQAPP}"
    python3 manage.py makemigrations
    python3 manage.py migrate

    # line below disabled
    # because admin user is created during wordpress installation
    # python3 manage.py create_admin_user

    mkdir -p "${DQAPP}/vendor"
    python3 manage.py download_vendor_files
    python3 manage.py collectstatic
    # python3 manage.py runserver 0.0.0.0:8000 &

else
    echo "Daiquiri is already installed."
fi
