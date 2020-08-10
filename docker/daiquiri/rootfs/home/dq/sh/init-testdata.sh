#!/bin/bash
set -e

cd "${DQAPP}"

python3 ./manage.py sqlcreate
python3 ./manage.py sqlcreate --test
python3 ./manage.py sqlcreate --schema=daiquiri_data_obs

python3 ./manage.py download_vendor_files
python3 ./manage.py test daiquiri --keepdb
python3 ./manage.py migrate
python3 ./manage.py migrate --database=data
python3 ./manage.py loaddata ../source/testing/fixtures/*
