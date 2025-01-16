#!/bin/bash

cd todo_list
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
gunicorn todo_list.wsgi