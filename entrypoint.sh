#!/usr/bin/env bash
python innotter/manage.py makemigrations user
python innotter/manage.py makemigrations page
python innotter/manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python innotter/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_USERNAME
fi
python innotter/manage.py runserver 0.0.0.0:8000
$@
