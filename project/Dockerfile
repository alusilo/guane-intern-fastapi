FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV SECRET_KEY='1ccd17edf4c5a2faf84b169cdff9aa9d205958f921d98bc0928cd510a948d689'
ENV ALGORITHM='HS256'

ENV DB_USER=dog_user
ENV DB_PASS=dog_pass
ENV DB_HOST=guane-db
ENV DB_NAME=dog
ENV DB_PORT=5432

ENV RABBITMQ_USER=rabbitmq_user
ENV RABBITMQ_PASS=rabbitmq_pass
ENV RABBITMQ_HOST=guane-rabbitmq
ENV RABBITMQ_PORT=5672

ENV REDIS_USER=redis_user
ENV REDIS_PASS=redis_pass
ENV REDIS_HOST=guane-redis
ENV REDIS_PORT=6379

COPY . .
