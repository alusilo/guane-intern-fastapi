# guane-intern-fastapi

This is app is developed using docker containers. To deploy the application it is neccessary to run the script ```build.sh``` locaited in the root directory. Run this script as follows:

```bash build.sh```

This initialize the construction of the docker containers. After finishing running this script are created the following dockers containers:

__guane-db__: PostgresSQL database container

__guane-redis__: Redis container

__guane-rabbitmq__: RabitMQ container

__guane-web__: API + Celery container

The documentation of the API is found accessing to http://127.0.0.1:8000/docs
