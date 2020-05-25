CURDIR=$(shell pwd)
DC_MASTER="dc_master.yaml"
DC_TEMP="docker-compose.yaml"

DOCKER_IN_GROUPS=$(shell groups | grep "docker")
MYID=$(shell id -u)

ifeq ($(strip $(DOCKER_IN_GROUPS)),)
	DC_CMD=sudo docker-compose
	D_CMD= sudo docker
else
	DC_CMD=docker-compose
	D_CMD=docker
endif

VARS_ENV=daiquiri/.env
GLOBAL_PREFIX=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=GLOBAL_PREFIX=).*")
QUERY_DOWNLOAD_DIR=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=QUERY_DOWNLOAD_DIR=).*")
ARCHIVE_BASE_PATH=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=ARCHIVE_BASE_PATH=).*")
DAIQUIRI_APP=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=DAIQUIRI_APP=).*")

WORDPRESS_DB_USER=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=WORDPRESS_DB_USER=).*")
WORDPRESS_DB_NAME=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=WORDPRESS_DB_NAME=).*")
WORDPRESS_DB_PASSWORD=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=WORDPRESS_DB_PASSWORD=).*")
WORDPRESS_DB_HOST=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=WORDPRESS_DB_HOST=).*")
DAIQUIRI_URL=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=DAIQUIRI_URL=).*")
WORDPRESS_URL=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=WORDPRESS_URL=).*")
HTTP_HOST=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=HTTP_HOST=).*")
SITE_URL=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=SITE_URL=).*")
DOCKERHOST=$(shell cat ${CURDIR}/${VARS_ENV} | grep -Po "(?<=DOCKERHOST=).*")
VARS_WP=wpdb/.env

all: root_check render_yaml preparations run_build tail_logs
build: render_yaml preparations run_build
fromscratch: render_yaml preparations run_remove run_build
remove: run_remove
restart: run_restart
down: run_down
log: tail_logs
yaml: render_yaml

root_check:
	@if [ "${MYID}" = "0" ]; then \
		echo Do not run as root. Conflicting file permissions will not allow it.; \
	fi
	@exit

render_yaml:
	cat ${DC_MASTER} \
		| sed 's|<HOME>|${HOME}|g' \
		| sed 's|<CURDIR>|${CURDIR}|g' \
		> ${DC_TEMP}

preparations:
	# wordpress config
	cat ${CURDIR}/daiquiri/conf/wp-config-sample.php \
		| sed 's|<WORDPRESS_URL>|"${WORDPRESS_URL}"|g' \
		| sed 's|<SITE_URL>|"${SITE_URL}"|g' \
		| sed 's|<HTTP_HOST>|"${HTTP_HOST}"|g' \
		| sed 's|<GLOBAL_PREFIX>|"${GLOBAL_PREFIX}"|g' \
		| sed 's|<WORDPRESS_DB_NAME>|"${WORDPRESS_DB_NAME}"|g' \
		| sed 's|<WORDPRESS_DB_USER>|"${WORDPRESS_DB_USER}"|g' \
		| sed 's|<WORDPRESS_DB_HOST>|"${WORDPRESS_DB_HOST}"|g' \
		| sed 's|<WORDPRESS_DB_PASSWORD>|"${WORDPRESS_DB_PASSWORD}"|g' \
		> ${CURDIR}/daiquiri/rootfs/tmp/wp-config-sample.php

run_build:
	$(DC_CMD) up --build -d

run_down:
	$(DC_CMD) -f ./docker-compose.yaml down -v

run_remove:
	$(DC_CMD) down
	$(DC_CMD) down -v
	$(DC_CMD) rm --force

tail_logs:
	$(DC_CMD) logs -f | grep -Ev '"GET / HTTP/1.1" 200'

run_restart:
	$(DC_CMD) restart
