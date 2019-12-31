#!/bin/sh
echo "Sleeping for 10s to ensure DB is online."
sleep 10  # Wait for DB to init -- hopefully
echo "Initializing DB"
venv/bin/python manage.py db init
echo "Detecting DB Delta"
venv/bin/python manage.py db migrate
echo "Upgrading DB"
venv/bin/python manage.py db upgrade
