#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input --clear

# 🟢 FORCE: Re-sync deployment app states across PostgreSQL
python manage.py makemigrations groceryapp
python manage.py migrate groceryapp --run-syncdb