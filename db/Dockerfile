FROM postgres:14-alpine

WORKDIR db

ENV POSTGRES_USER="dog_user"
ENV POSTGRES_PASSWORD="dog_pass"
ENV POSTGRES_DB="dog"

ADD setup.sql /docker-entrypoint-initdb.d/
