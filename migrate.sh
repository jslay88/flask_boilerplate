#!/usr/bin/env sh

# make sure pg is ready to accept connections
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"
do
  echo "Waiting for postgres at: $POSTGRES_HOST:$POSTGRES_PORT"
  sleep 2;
done

if ! test -z "$BUILD_MIGRATIONS"; then
  echo "Building Migrations..."
  python manage.py db migrate
fi

echo "Applying Migrations (if any)..."
python manage.py db upgrade
