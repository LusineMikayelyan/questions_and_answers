#!/bin/bash

python qanda_project/manage.py makemigrations
python qanda_project/manage.py migrate --noinput
python qanda_project/manage.py collectstatic --noinput
python qanda_project/manage.py runserver 0.0.0.0:8000