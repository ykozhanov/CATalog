#!/bin/bash

# Завершить выполнение скрипта при ошибке
set -e

# Функция для обработки ошибок
error_exit() {
    echo "Ошибка: $1"
    exit 1
}

# Получаем текущую директорию
current_dir="$PWD"

# Переходим в родительскую директорию
parent_dir="$(dirname "$current_dir")"

# Устанавливаем PYTHONPATH
export PYTHONPATH="$parent_dir"

# Применяем миграции
cd alembic_backend/ && alembic upgrade head || error_exit "Не удалось выполнить миграцию в alembic_backend"
cd ../alembic_notification_telegram/ && alembic upgrade head || error_exit "Не удалось выполнить миграцию в alembic_notification_telegram"
cd ../alembic_telegram/ && alembic upgrade head || error_exit "Не удалось выполнить миграцию в alembic_telegram"

echo "Миграции применены!"
