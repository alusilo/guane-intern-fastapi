#!/bin/bash

docker-compose up -d db
docker-compose up -d redis
docker-compose up -d rabbitmq
docker-compose up -d web
docker-compose up -d worker
