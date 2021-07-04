#!/bin/sh -ex

python manage.py collectstatic --no-input

/app/docker/wait-for-it.sh ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}

python manage.py migrate

# Дамп БД
python manage.py loaddata providers products offers users

# Файлы медиа
tar -xzf /app/docker/screenshots.tar.gz -C /app/media/ screenshots

exec "$@"
