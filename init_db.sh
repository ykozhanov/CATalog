#!/bin/bash

# Функция для проверки доступности базы данных
wait_for_db() {
    while ! nc -z ${DB_HOST} ${DB_PORT}; do
        echo "Ожидание запуска базы данных..."
        sleep 1
    done
    echo "База данных доступна!"
}

# Ожидание базы данных
wait_for_db

# Запуск PostgreSQL в фоновом режиме
postgres &

# Ожидание, чтобы сервер PostgreSQL успел запуститься
sleep 10

# Создание баз данных
psql -U user -c "CREATE DATABASE ${DB_NAME_BACKEND};"
psql -U user -c "CREATE DATABASE ${DB_NAME_FRONTEND_TELEGRAM};"
psql -U user -c "CREATE DATABASE ${DB_NAME_FRONTEND_NOTIFICATION_SERVICE};"

# Ожидание завершения процесса PostgreSQL
wait