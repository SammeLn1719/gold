#!/bin/bash

echo "🚀 Запуск Django проекта в Docker..."
echo ""

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка наличия Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"
echo ""

# Проверка .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создание из .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Файл .env создан. Отредактируйте его при необходимости."
    else
        echo "❌ Файл .env.example не найден!"
        exit 1
    fi
fi

echo "📦 Сборка Docker образов..."
docker-compose build

echo ""
echo "🐳 Запуск контейнеров..."
docker-compose up -d

echo ""
echo "⏳ Ожидание готовности базы данных..."
sleep 5

echo ""
echo "🗄️  Применение миграций..."
docker-compose exec -T web python manage.py migrate

echo ""
echo "📊 Сбор статических файлов..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo "✅ Проект успешно запущен!"
echo ""
echo "📍 Доступные адреса:"
echo "   🌐 Главная страница: http://localhost:8000/"
echo "   🔐 Админ-панель:     http://localhost:8000/admin/"
echo ""
echo "💡 Создайте суперпользователя командой:"
echo "   docker-compose exec web python manage.py createsuperuser"
echo "   или: make createsuperuser"
echo ""
echo "📋 Просмотр логов:"
echo "   docker-compose logs -f"
echo "   или: make logs"
echo ""
echo "🛑 Остановка проекта:"
echo "   docker-compose down"
echo "   или: make down"
echo ""



