SHELL := /bin/bash

run: build

# docker
build:
	docker-compose build && \
	docker-compose up -d

down:
	docker-compose down --remove-orphans



# build:  
# 	docker build -t docker_app .

# run:
# 	docker run -p 6000:5000 -d $(argument)

