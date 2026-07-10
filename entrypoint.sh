#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "##########"
    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py migrate

# Superuser creation is an explicit deployment choice, not an operation that
# should run on every container start.
if [ "${DJANGO_CREATE_SUPERUSER:-False}" = "True" ]; then
    python manage.py createsuperuser --noinput
fi


exec "$@"
