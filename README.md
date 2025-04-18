# CATalog
Исполнитель: **Юрий Кожанов**

-------------------------------------------------------------------------------------

## Содержание
1. [Описание](#описание-проекта)
2. [Установка](#установка-и-запуск)
3. [Скриншоты](#скриншоты-приложения)
4. [Инструменты](#используемые-инструменты)
5. [Контакты](#контакты)


## Описание проекта
Домашний каталог вещей с базовыми возможностями. Frontend часть реализована как телеграм бот.

Возможности пользователя в телеграм боте:
- Создать категорию товара
- Редактировать категорию товара
- Удалить категорию товара (сохранить / удалить связанные товары)
- Получить список товаров в категории
- Создать товар
- Редактировать товар
- Использовать товар (при полном использовании товар удаляется)
- Удалить товар
- Получить список всех категорий
- Получить список всех товаров
- Получить список товаров по названию
- Получить список товаров у которых заканчивается скор годности


В сервисе предусмотрена регистрация и аутентификация через **JWT Token**, пароли пользователей хэшируются перед записью в базу данных.

В качестве frontend используется telegram бот написанный на библиотеке **pyTelegremBotAPI**.


Сервисом предусмотрено отправка уведомлений пользователю о скором окончании срока годности (через **Celery Beat**). 

Сервис уведомлений создан как микросервис в котором, при необходимости, можно реализовать другие способы уведомлений (взаимодействие через **Kafka**).


Приложение запускается через **Docker Compose** и не теряет данные между перезапусками (данные хранятся в **PostgreSQL**).


## Установка и запуск
### Шаг 1: Предварительная настройка
Перед использованием приложения убедитесь, что на Вашем устройстве (Linux-based OS) установлен **Docker 28.0.1**

### Шаг 2: Клонируйте репозиторий
Клонируйте github репозиторий на Ваше устройство:
```bash
git clone https://github.com/ykozhanov/CATalog.git
```

### Шаг 3: Настройка переменных окружения
- Перейдите в директорию с репозиторием:
```bash
cd CATalog
```
- Создайте `.env` файл с переменными. Для примера используйте `.env-example` из репозитория.

- Для генерации RSA ключей можете использовать команды:
    - `openssl genrsa -out jwt-private.pem 2048`
    Эта команда генерирует закрытый ключ RSA длиной 2048 бит и сохраняет его в файл jwt-private.pem.
    
    - `openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem`
    Эта команда извлекает открытый ключ из ранее сгенерированного закрытого ключа, который хранится в файле jwt-private.pem.

### Шаг 4: Docker-Compose
- Для запуска выполните в терминале: 
```bash 
docker compose up
```

### Шаг 5. Применение миграций
После запуска всех контейнеров (ориентируйтесь на celery-контейнер) примените миграции к базе данных.
Для этого выполните скрипт `migrate.sh` из директории `alembic` (Предварительно установив библиотеку alembic на устройство).

**Важно**: Запускать скрипт необходимо из директории `alembic`.


## Скриншоты приложения
**Регистрация**

![Регистрация](screenshots/screenshot_1.png)
***

**Создание нового товара**

![Создание нового товара](screenshots/screenshot_2.png)
***

**Список товаров**

![Список товаров](screenshots/screenshot_3.png)
***

**Список категорий**

![Список категорий](screenshots/screenshot_4.png)
***

**Информация о категории**

![Информация о категории](screenshots/screenshot_5.png)
***

**Информация о товаре**

![Информация о товаре](screenshots/screenshot_6.png)
***

**Список товаров у которых заканчивается срок годности**

![Список товаров у которых заканчивается срок годности](screenshots/screenshot_7.png)
***

**Использование товара**

![Использование товара](screenshots/screenshot_8.png)
***

**Полное использование товара**

![Полное использование товара](screenshots/screenshot_9.png)
***

**Список товаров без полностью использованного товара**

![Список товаров без полностью использованного товара](screenshots/screenshot_10.png)
***


## Используемые инструменты
- [Python](https://www.python.org/) как основной язык программирования;
- [FastAPI](https://flask.palletsprojects.com/) как backend сервиса;
- [PostreSQL](https://www.postgresql.org/) как база данных;
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/) как ORM инструмент;
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) как инструмент миграций базы данных;
- [Celery](https://docs.celeryq.dev/) как инструмент выполнения фоновых задач (уведомлений о товарах у которых заканчивается срок годности);
- [Redis](https://github.com/redis/redis) как брокер сообщений для фоновых задач;
- [Docker](https://www.docker.com/) для контейнеризации приложения.


## Контакты
По вопросам проекта и другим вопросам связанным с используемыми в проекте инструментам 
можно писать на почту `ykozhanov97@gmail.com`
