#!/usr/bin/env bash

cd /home/kestas/ptu5_django_library/ptu5_library
source ../venv/bin/activate
gunicorn ptu5_library.wsgi --bind 0.0.0.0:8000
