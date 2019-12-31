#!/bin/sh

venv/bin/uwsgi --http :5000 --wsgi-disable-file-wrapper --manage-script-name --mount /=run:app
