# django_ishop

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5-green.svg)
![Poetry](https://img.shields.io/badge/Poetry-enabled-60A5FA)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**django_ishop** --- учебный проект интернет-магазина с блогом,
каталогом товаров, пользовательскими аккаунтами и отправкой писем.\
Стек: **Django 5**, **Poetry**, **Bootstrap**, **PostgreSQL**.

##  Содержание

-   [Описание](#описание)
-   [Структура проекта](#структура-проекта)
-   [Установка и запуск](#установка-и-запуск)
-   [Быстрый старт](#быстрый-старт)
-   [Работа с пользователями](#работа-с-пользователями)
    -   [Регистрация](#регистрация)
    -   [Отправка писем](#отправка-писем)
    -   [Авторизация](#авторизация)
    -   [Ограничение доступа](#ограничение-доступа)
-   [Заполнение БД (фикстуры)](#заполнение-бд-фикстуры)
-   [Админ-панель](#админ-панель)
-   [Проверка данных](#проверка-данных)
-   [CRUD продуктов](#crud-продуктов)
-   [Валидация форм](#валидация-форм)
-   [Работа с изображениями](#работа-с-изображениями)
-   [Приложение блога](#приложение-блога)
-   [Технологии](#технологии)
-   [Лицензия](#лицензия)

##  Описание

Проект включает:

-   каталог товаров (CRUD, валидация, изображения);
-   блог с публикациями и счётчиком просмотров;
-   кастомную модель пользователя с аватаром и email-авторизацией;
-   регистрацию и отправку приветственных писем;
-   авторизацию и защиту доступа;
-   Django админку;
-   фикстуры и кастомные команды.

##  Структура проекта

    django_ishop/
    ├─ catalog/
    ├─ blogera/
    ├─ users/
    ├─ config/
    ├─ static/
    ├─ media/
    └─ manage.py

## ⚙ Установка и запуск

    git clone https://github.com/botnbot/django_ishop.git
    cd django_ishop
    pip install poetry
    poetry install
    poetry shell

Настрой .env:

    SECRET_KEY=...
    DEBUG=True
    DATABASE_NAME=...
    DATABASE_USER=...
    EMAIL_HOST_USER=YOUR_EMAIL@gmail.com
    EMAIL_HOST_PASSWORD=APP_PASSWORD

##  Быстрый старт

    python manage.py migrate
    python manage.py collectstatic --noinput
    python manage.py runserver

##  Работа с пользователями

###  Кастомная модель пользователя

Используется модель: `users.CustomUser`.

Поля: email, username, phone_number, avatar, country.

###  Регистрация

Форма на `/users/register/`.

###  Отправка писем

Используется `send_mail()` и SMTP.

###  Авторизация

Страница: `/users/login/`.

###  Ограничение доступа

Создание/редактирование товаров --- только авторизованные.

##  Заполнение БД (фикстуры)

    python manage.py loaddata categories
    python manage.py loaddata products

##  Админ-панель

    python manage.py createsuperuser

##  Проверка данных

    from catalog.models import Product
    Product.objects.all()

##  CRUD продуктов

-   список `/products/`
-   создание `/products/create/`
-   просмотр, редактирование, удаление

##  Валидация форм

Запрещённые слова + проверка цены.

##  Работа с изображениями

Загрузка, сохранение, удаление.

##  Приложение блога

CRUD, статус публикации, счётчик просмотров.

## Технологии

Python, Django, PostgreSQL, Poetry, Bootstrap.

## Лицензия

MIT License.
