CONF_FILE=$(shell if [ -f conf_local.yaml ]; then echo conf_local.yaml; else echo conf.yaml; fi)
CURDIR=$(shell pwd)
DC_MASTER="dc_master.yaml"
DC_TEMP="docker-compose.yaml"

DOCKER_IN_GROUPS=$(shell groups | grep "docker")

ifeq ($(strip $(DOCKER_IN_GROUPS)),)
	DC_CMD=sudo docker-compose
	D_CMD= sudo docker
else
	DC_CMD=docker-compose
	D_CMD=docker
endif

all: render_yaml run_build tail_logs
build: render_yaml run_build
fromscratch: render_yaml run_remove run_build
remove: run_remove
restart: run_restart
down: run_down
log: tail_logs
yaml: render_yaml

render_yaml:
	python3 ./py/render_yaml.py ${CONF_FILE}

run_build:
	$(D_CMD) volume rm dq_app || :
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
