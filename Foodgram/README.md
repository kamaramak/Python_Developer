# Foodgram - «Продуктовый помощник»
Проект представляет из себя сервис по созданию, хранению и поиску рецептов. Сервис позволяет авторам создавать свои рецепты, а пользователям - подписываться на других авторов и добавлять рецепты в избранное, создавать список покупок, который можно скачать в виде txt файла.

## Спецификация API располагается по адресу https://kamaramak.github.io/foodgram_docs/

## Авторы проекта:
    - backend: Кабардоков Марат
    - frontend: команда Яндекс Практикума.
## Стек:
    - **backend**: python 3.12, Django 5.2, DRF 3.16;
    - **database**: PostgreSQL 14;
    - **Web Server**: nginx;
    - **Container**: Docker;

## Локальное развертывание:

### 1. Предварительные требования:

```bash
git clone git@github.com:yandex-praktikum/foodgram.git
cd foodgram
```

### 2. Запустить проект с помощью docker:
Создание и запуск docker-образов:
```bash
docker compose up -d
```
Настройка базы данных:
```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py load_data
docker compose exec backend python manage.py collectstatic --no-input
```

### Доступ к приложению:
Сервис доступен по адресу: https://kamar-foodgram.ddns.net
Администраторская зона доступна по адресу: https://kamar-foodgram.ddns.net/admin/
