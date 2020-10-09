#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "##########"
    echo "PostgreSQL started"
fi

rm -r /code/static/*  # clears static files (if something should have changed in new deployment)

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py migrate dynamic_preference
python manage.py createsuperuser --noinput


exec "$@"