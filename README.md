# foodgram-project
foodgram-project

# GitHub Actions Result

Status of Last Deployment: <br>:
<img src="https://github.com/Knoort/workflows/foodgram-workflow/badge.svg?branch=master"><br>

Работающее приложение:
http://foodmanager.cf/recipes/

## Описание
Это учебный проект сайта "Продуктовый помощник" с Continious Integration.
Сервис позволяет создавать рецепты с картинками, выбирать понравившиеся рецепты, подписываться на
других авторов, 

После развертывания сервис проекта доступен по адресу:
http:/{host_name}/recipes/
Панель управления администратора находится по адресу:
http://{host_name}/admin/

## Развертывание
В среде сервера для запуска приложения должны быть установлены сервисы git, docker, скрипт docker-compose версии не ниже 1.27.4. Необходим аккаунт GitHub.
* Проверка версии docker-compose:
    - docker-compose --version
* Обновление версии:
    - sudo curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    - sudo chmod +x /usr/local/bin/docker-compose

* Скопировать в папку для установки приложения любым доступным способом 3 файла из репозитория:
    - docker-compose.yaml
    - entrypoint.sh
    - nginx/default.conf (соблюдая указанный путь)
* Создать файл с переменными окружения .env в главном каталоге проекта, по аналогии с приложенным образцом
    .env_sample
* Для первого запуска приложения, в папке с скопированными файлами использовать команду: 
    - docker-compose up -d
* Для повторного запуска после обновления, использовать команды:
    - docker-compose down
    - docker-compose up -d

После скачивания образов, приложение будет развернуто в 3-х контейнерах и готово к приему команд.

Для настройки проекта после первичной установки необходимо провести настройку статического содержимого. Для доступа к панели администрирования необходимо создание суперпользователя. Эти действия производятся внутри запущенного контейнера с самим приложением yamdb_final, имеющего суффикс "web". 

* Вывести список запущенных контейнеров после запуска приложения:
    - docker container ls

* Команда для входа в контейнер yamdb_final:
    - docker exec -it <CONTAINER ID[:4]> sh, или
    - docker exec -it <CONTAINER NAME> sh,
    где <CONTAINER ID[:4]> - первые 4 (или больше) знаков ID контейнера с приложением yamdb_final,
    <CONTAINER NAME> - имя контейнера с приложением  yamdb_final, созданное по шаблону <Имя каталога проекта>_web_1.

Все действия по настройке выполняются из папки /code контейнера, в которую производится вход в контейнер по умолчанию.

* Загрузка статики:
    - python manage.py collectstatic
* Создание суперпользователя:
    - python manage.py createsuperuser;

## Создано с помощью

* [Django](https://docs.djangoproject.com/en/3.1/) - Python веб фреймворк
* [Django REST framework](https://www.django-rest-framework.org/) - 
Библиотека для создания REST-сервисов на основе Django
* [Docker]((https://www.docker.com) - контейнеризация приложений.
* [GithubActions](https://docs.github.com/en/free-pro-team@latest/actions) - 
Платформа автоматической интеграции разработки. (Continious Integration technology).


## Авторы, контактная информация

* **Дмитрий Струнин** - *Team leader, разработчик* - (https://github.com/Knoort)
Электронная почта - m-kris@narod.ru

## Благодарности

Спасибо всей команде Яндекс.Практикум, наставникам, ревьюерам и разработчикам за их обширную работу и постоянную помощь.
Отдельная благодарность наставникам **Владиславу Шевченко**, **Алексею Гайбуре**, ревьюеру **Максиму Любиеву** за живое участие.
