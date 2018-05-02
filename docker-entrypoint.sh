#!/bin/sh

cp /usr/share/zoneinfo/GB /etc/localtime

#Collect static resources
echo "Collecting static assets"
python manage.py collectstatic --settings=$PROJECT_SETTINGS --noinput

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000 --settings=$PROJECT_SETTINGS
