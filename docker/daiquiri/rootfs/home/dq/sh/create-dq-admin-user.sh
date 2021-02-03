#!/bin/bash

USER="${DAIQUIRI_ADMIN_USER}"
PASS="${DAIQUIRI_ADMIN_PASSWORD}"
MAIL="${DAIQUIRI_ADMIN_EMAIL}"

echo "Create daiquiri admin user"

script="
from django.contrib.auth.models import User;

username = '${USER}';
password = '${PASS}';
email = '${MAIL}';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"

cd "${DQAPP}"
printf "${script}" | python manage.py shell
