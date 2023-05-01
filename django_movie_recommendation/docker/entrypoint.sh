#!/bin/bash

cd django_movie_recommendation

python manage.py migrate

python manage.py runserver 0.0.0.0:7777
