SHELL := /bin/bash

check-var = $(if $(strip $($1)),,$(error var for "$1" is empty))

default: help

help:
	@gawk 'BEGIN {FS= ":.*?## "} /^\S+:(.*)?##/ { printf "  %-20s\t%-20s\n", $$1, $$2}' ${MAKEFILE_LIST}

docker-build: ## build a docker container
	@docker build -t python-rest .

docker-run: ## run a docker container
	@docker run -d -p 80:8000 python-rest

check-port80:  ## check port 80
	@nc -vzw3 localhost 80

healthcheck: ## run health check
	@curl http://localhost/healthcheck

upload-data: healthcheck ## upload a test data
	@curl -d @words http://localhost/records

run-test: upload-data ## run a python script to start multiple request against rest url
	@python multi.py

stop-container: ## stop a docker container
	@docker ps -a | grep -v 'CONTAINER' | grep python-rest | awk '{ print $$1 }' | xargs docker container stop

clean: stop-container ## remove docker container
	@docker ps -a | grep -v 'CONTAINER' | grep python-rest | awk '{ print $$1 }' | xargs docker container rm

%:
	@echo "ignoring rule $@" >/dev/null
