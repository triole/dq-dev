#!/bin/bash

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $(pip3 freeze | grep -Poc "django-daiquiri") == "0" ]]; then

    cd "${DQSOURCE}" || exit 1
    pip3 install -e "${DQSOURCE}"

    cd "${DQAPP}"
    python3 manage.py makemigrations
    python3 manage.py migrate

    # silent because of the error message, that wp admin user already exists
    # necessary to create the daiquiri admin user
    # python3 manage.py create_admin_user >/dev/null 2>&1
    # create the same user than wordpress one (done with shell because createsuperuser do not accept inline passwords)
    python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('dqadmin', 'dqadmin@sirrah.de', '4fb4cb000853f6cc7a6012202d2af4e3')" >/dev/null 2>&1
    # DJANGO_SUPERUSER_PASSWORD=1234; python3 manage.py createsuperuser --username yori --email yori@sirrah.com --noinput; # this does not work...

    mkdir -p "${DQAPP}/vendor"
    python3 manage.py download_vendor_files
    python3 manage.py collectstatic >/dev/null 2>&1
    # python3 manage.py runserver 0.0.0.0:8000 &

else
    echo "Daiquiri is already installed."
fi
