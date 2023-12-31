# Web_portal_for_financial_management
![Python](https://img.shields.io/badge/-Python-f1f518?style=flat-square&logo=python)
![Fkask](https://img.shields.io/badge/-Flask-74cf3c?style=flat-square&logo=flask) 
![Bootstrap](https://img.shields.io/badge/-Bootstrap-ce62f5?style=flat-square&logo=bootstrap)
![Docker](https://img.shields.io/badge/-Docker-1de4f2?style=flat-square&logo=docker)  
![Redis](https://img.shields.io/badge/-Redis-f78b97?style=flat-square&logo=redis)
![Postgresql](https://img.shields.io/badge/-Postgresql-1de4f2?style=flat-square&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-ba7378?style=flat-square&logo=sqlalchemy)
![Alembic](https://img.shields.io/badge/-Alembic-80cced?style=flat-square&logo=Alembic)

Приложение для контроля финансов
* приложение позволяет создавать счета
* создовать транзакции
* показывать количество созданных счетов
* общий баланс по всем счетам
* показывать транзакции по конкретному счету



### Установка

Необходимо создать в корне проекта файл .env в котором указать: 
POSTGRES_DB=ваше_название_для базы данных 

POSTGRES_HOST=weather_database 

POSTGRES_USER=ваше_имя_пользователя 

POSTGRES_PASSWORD=ваш_пароль 

POSTGRES_PORT=(можете указать другой порт-тогда и в docker-compose.yml необходимо изменить на другой) 

REDIS_HOST=web_portal_redis - если запускает через docker 

REDIS_PORT=6112 - или укажите свой(тогда необходимо изменить и в docker-compose.yml)

REDIS_DB=0 

SECRET_KEY_FOR_CSRF=секретный_ключ_для_csrf_токена 

#### Установка на локальный компьютер
git clone https://github.com/Victor-Krupeichenko/Web_portal_for_financial_management.git
pip install -r requirements.txt
запуск через терминал:
под linux export FLASK_APP=app.py
под window $env:FLASK_APP = app.py
flask run
перейти по ссылке: http://127.0.0.1:5000
#### Установка в docker
git clone https://github.com/Victor-Krupeichenko/FlaskMail.git
запуск через терминал(обязательно должны находится в папке проекта): docker compose up или docker-compose up
перейти по ссылке: http://127.0.0.1:5011

После запуска приложения в корневой папке будет создана папка postgres_data - в ней хранится локальная версия базы данных

### Структура проекта
В папке account находятся:
* Форма для создания счета
* endpoints для взаимодейстия со счетом

В папке analytics находится:
* endpoints для просмотра баланса и количества созданных счетов

В папке database находятся:
* подключение к базе данных
* модели таблиц базы данных
* адрес базы данных

В папке docker_start находится:
* sh-скрипт для запуска приложения

В папке errors находятся:
* endpoints для страниц с ошибками

В папке migrations находятся:
* версия миграции для создания таблиц в базе данных
* настройки имен переменного окружения для подключения к базе данных

В папке static находятся:
* файл стилей .css
* статическое изображение

В папке templates находятся
* HTML-шаблоны страниц

В папке transactions находятся:
* форма для создания транзакций
* endpoints для работы с транзакциями

В папке user находятся:
* формы для взаимодействия с пользователем
* endpoints для авторизации, регистрации и тд.
* endpoints для смены пароля и удаление пользователя

alembic.ini содержит маршрут для подключения alembic к базе данных

docker-compose.yml содержит описание запуска проекта в docker

Dockerfile содержит инструкции для создания docker-образа

app.py это файл в котором находятся нстройки самого приложения

requirements.txt в нем находятся все необходимые для работы приложения библиотеки и зависимости

env_settings.py - настройки имен переменно окружения

settings_cached.py - настройки кэширования под redis

utils.py - содержит различные вспомогательные функции

### Контакты:
* Виктор

#### Email:
* krupeichenkovictor@gmail.com
* victor_krupeichenko@hotmail.com
#### Viber:
* +375447031953
