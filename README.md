# multi-url-request

This is a python REST application that can take a multiple requests concurrently.

## requirement

The python application is running from a Docker container. To successfully run this python application, you need
to install the following tools,

* docker - installed from [docker.io](https://www.docker.com/)
* python >= 3.7 - the python code is written and in python3, make sure you have proper python interpreter installed on your system
** python requests library - this is required for submitting multiple requests to the api server. You can run `pip install requests`
* nc (netcat) - check to see if a given port is listening
* curl - a utility for interact with api server

## running a container and submitting requests

We parepare a Makefile to simplify the process of building and running the docker container. cd into `multi-url-request` dirctory, and
run `make` command, and it will print out the help message like this,

    docker-build     build a docker container
    docker-run       build a docker container
    check-port80     check to see if port 80 is running
    healthcheck      run health check
    upload-data      upload a test data
    run-test         run a python script to start multiple request against rest url
    stop-container   stop a docker container
    clean            remove docker container

### make docker-build and make docker-run

* make docker-build builds a docker container
* make docker-run runs a docker container

### make check-port80 and health check

* make check-port80 use `nc` to check port 80 for a given system. This ensure service is listening (this one does not show when you run make without parameters)
* make healthcheck use curl to hit api endpoint http://localhost/healthcheck to ensure server is functioning

### make upload-data and make run-test

* make upload-data use curl to upload words file to the server
* make run-test execute a python script multi.py to submit 1000 unique url calls to server

### make clean

make clean depends on `stop-container` to first stop the container and them remove it from the process table
