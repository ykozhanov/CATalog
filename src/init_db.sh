#!/bin/bash

# Выход при ошибке
set -e

# Создание баз данных
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE ${DB_NAME_BACKEND};
    CREATE DATABASE ${DB_NAME_FRONTEND_TELEGRAM};
    CREATE DATABASE ${DB_NAME_NOTIFICATION_SERVICE};
EOSQL
