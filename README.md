# Foodgram - сайт 'Продуктовый помощник'

------------
![example workflow](https://github.com/turpanov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Описание проекта
Сервис предоставляет пользователям возможность публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

------------

## Используемые технологии:
- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker
------------
## Установка и запуск проекта
Выполните установку git, docker и docker-compose
```sh
sudo apt install git docker docker-compose -y
```
Клонируйте репозиторий и перейдите в его директорию:
```sh
git clone git@github.com:turpanov/foodgram-project-react.git
cd foodgram-project-react
```
Для работы с базой данных перейдите в директорию infra и создайте в ней .env файл с переменными окружения.

В директории infra отредактируйте файл nginx.conf: в поле server_name укажите IP адрес вашего сервера.
```
server {
  server_tokens off;
  listen 80;
  server_name <SERVER_IP>;
```
Выполните запуск контейнеров
```sh
sudo docker compose up -d
```
После запуска контейнеров выполните миграции и сборку статики
```sh
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создание суперпользователя:
```sh
sudo docker compose exec backend python manage.py createsuperuser
```
Проверьте доступность проекта по адресу, указанному в конфигурации ```http://<SERVER_IP>```


------------


## Автор проекта

Андрей Турпанов
студент 31 когорты факультета Python разработки
Yandex Practicum
