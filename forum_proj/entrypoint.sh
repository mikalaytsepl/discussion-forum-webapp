#!/bin/bash
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}

echo "Waiting for database at $DB_HOST:$DB_PORT..."
sleep 10
echo "slepped for 10 seconds, proceeding with migrations"
#while ! nc -z $DB_HOST $DB_PORT; do
#  sleep 0.1
#done

echo "Database Started"

python manage.py makemigrations
python manage.py migrate

exec "$@"