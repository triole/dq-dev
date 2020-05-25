# manual settings
CURDIR=$(shell pwd)
VOLTOOLS="$(shell pwd | grep -Po ".*(?=\/)")/voltools"

DC_MASTER="${CURDIR}/dc_master.yaml"
DC_TEMP="${CURDIR}/docker-compose.yaml"

all: prep run_build tail_logs
build: prep run_build
fromscratch: run_remove prep run_build
remove: run_remove
prep: render_dockerfile

render_dockerfile:
	cat dockerfile_master \
	> dockerfile

run_build:
	sudo docker-compose up --build -d

run_remove:
	sudo docker-compose down --rmi all
	sudo docker-compose rm --force

tail_logs:
	sudo docker-compose logs -f
