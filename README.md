# Команды для запуска

```bash
# 1. Клонирование репозитория
git clone <repository-url>
cd django-ecommerce

# 2. Создание .env файла
cat > .env << EOF
POSTGRES_DB=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
EOF

# 3. Запуск контейнеров
docker-compose up --build

# 4. В новом терминале - миграции
docker-compose exec web python manage.py migrate

# 5. Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# 6. Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput
```

## Доступ к приложению

- **Сайт**: http://localhost:8000

## Остановка

```bash
docker-compose down
```

## Очистка

```bash
docker-compose down -v
docker system prune -a
```