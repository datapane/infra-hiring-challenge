#!/bin/sh


cd /app

redis-server &> /var/log/redis_server.log &

celery -A  app.celery worker -f /var/log/celery.log --loglevel INFO &


#export FLASK_APP=app

#export FLASK_APP="src.app:create_app"
#flask run --host=0.0.0.0 --port=8080

#gunicorn --chdir /app src.app:create_app -w 2 --threads 2 -b 0.0.0.0:8080

gunicorn --chdir /app app:app -w 2 --threads 2 -b 0.0.0.0:8080 --log-file /var/log/gunicorn_err.log --access-logfile /var/log/gunicorn_acc.log &


if [ "$APP_TESTING" = "TRUE" ]; then
    sleep 2
    echo "Starting testing"
    python -m unittest -v
    exit $?

fi

while [ 1 ]
do
   sleep 1
done