#!/bin/bash

# Режим запуска: docker или venv
MODE=${1:-auto}

echo "🚀 Запуск Django проекта..."
echo ""

# Функция для запуска через Docker
start_with_docker() {
    echo "📦 Режим: Docker"
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
    echo "💡 Если сборка прерывается, попробуйте:"
    echo "   docker-compose build --no-cache --progress=plain"
    echo ""
    docker-compose build --progress=plain
    
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
}

# Функция для запуска через venv
start_with_venv() {
    echo "🐍 Режим: Virtual Environment (venv)"
    echo ""
    
    # Проверка Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 не установлен. Пожалуйста, установите Python 3.8+."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "✅ Найден Python версии $PYTHON_VERSION"
    echo ""
    
    # Создание виртуального окружения, если его нет
    if [ ! -d "venv" ]; then
        echo "📦 Создание виртуального окружения..."
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo "❌ Ошибка при создании виртуального окружения!"
            echo "💡 Установите пакет venv: sudo apt install python3-venv"
            exit 1
        fi
        echo "✅ Виртуальное окружение создано"
    else
        echo "✅ Виртуальное окружение уже существует"
    fi
    echo ""
    
    # Активация виртуального окружения
    echo "🔌 Активация виртуального окружения..."
    source venv/bin/activate
    
    # Обновление pip
    echo "📦 Обновление pip..."
    pip install --upgrade pip -q
    
    # Установка зависимостей
    echo "📦 Установка зависимостей из requirements.txt..."
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Ошибка при установке зависимостей!"
            exit 1
        fi
        echo "✅ Зависимости установлены"
    else
        echo "❌ Файл requirements.txt не найден!"
        exit 1
    fi
    echo ""
    
    # Создание .env файла, если его нет
    if [ ! -f .env ]; then
        echo "⚠️  Файл .env не найден. Создание базовой конфигурации..."
        cat > .env << EOF
DEBUG=True
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EOF
        echo "✅ Файл .env создан"
    fi
    echo ""
    
    # Применение миграций
    echo "🗄️  Применение миграций..."
    python manage.py migrate
    if [ $? -ne 0 ]; then
        echo "❌ Ошибка при применении миграций!"
        exit 1
    fi
    echo ""
    
    # Сбор статических файлов
    echo "📊 Сбор статических файлов..."
    python manage.py collectstatic --noinput
    echo ""
    
    echo "✅ Проект готов к запуску!"
    echo ""
    echo "📍 Для запуска сервера выполните:"
    echo "   source venv/bin/activate"
    echo "   python manage.py runserver"
    echo ""
    echo "💡 Создайте суперпользователя командой:"
    echo "   source venv/bin/activate"
    echo "   python manage.py createsuperuser"
    echo ""
    echo "🌐 После запуска проект будет доступен:"
    echo "   Главная страница: http://localhost:8000/"
    echo "   Админ-панель:     http://localhost:8000/admin/"
    echo ""
    echo "🚀 Запуск сервера разработки..."
    python manage.py runserver
}

# Определение режима запуска
if [ "$MODE" = "docker" ]; then
    # Принудительный запуск через Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker не установлен. Пожалуйста, установите Docker."
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
        exit 1
    fi
    start_with_docker
elif [ "$MODE" = "venv" ]; then
    # Принудительный запуск через venv
    start_with_venv
else
    # Автоматический выбор режима
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        echo "🔍 Обнаружен Docker. Используется Docker-режим."
        echo "💡 Для использования venv запустите: ./start.sh venv"
        echo ""
        start_with_docker
    elif command -v python3 &> /dev/null; then
        echo "🔍 Docker не найден. Используется venv-режим."
        echo ""
        start_with_venv
    else
        echo "❌ Не найден ни Docker, ни Python3!"
        echo "Установите один из них для запуска проекта."
        exit 1
    fi
fi



