#!/bin/bash

# Ожидание готовности PostgreSQL
echo "Ожидание готовности PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(host='db', port=5432, user='${DB_USER}', password='${DB_PASSWORD}', dbname='${DB_NAME}')" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL запущен"

# Применение миграций
echo "Применение миграций..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Сбор статических файлов..."
python manage.py collectstatic --noinput

# Создание суперпользователя (если нужно)
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Запуск команды
exec "$@"



