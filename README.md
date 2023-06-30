# Foodgram - Grocery Assistant.
Service for publishing and sharing recipes
Here you can subscribe to your favorite authors and save your favorite recipes,
and before going to the store - download a list of products needed for the present.

## Technology stack
![Django-app workflow](https://github.com/Alexey-zaliznuak/foodgram-project-react/actions/workflows/main.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)


## Environment Variables

To run this project, you will need to add the following environment
variables to your .env file. See template in .env.dist file.

### Main backend settings

`SECRET_KEY`

`DEBUG` (default - 'True')

`IP` (your server IP), not required

`URL` (your server URl), not required

`TIME_ZONE` (default - 'UTC')

`USE_TZ` (default - 'True')

`DATABASE` (POSTGRES/SQLIE, default - POSTGRES)

### Postgres settings

`POSTGRES_DB` (default - 'foodgram')

`POSTGRES_USER` (default - 'foodgram_user')

`POSTGRES_PASSWORD` (default - 'foodgram_password')

`POSTGRES_HOST` (default - 'db')

`POSTGRES_PORT` (default - '5432')

### Django superuser information for auto create

`DJANGO_SUPERUSER_EMAIL` (default - email10@gmail.com)

`DJANGO_SUPERUSER_PASSWORD` (default - password)

`DJANGO_SUPERUSER_USERNAME` (default - username)

## Installation

### Run on the local mashine

#### In project folder make and activate virtual environment
Linux/MacOS:
```
python3 -m venv env
```
Windows
```
python -m venv env
```

#### Activate the environment
Linux/MacOS:
```
source venv/bin/activate
```
Windows:
```
.\venv\Scripts\activate
```

Go to backend folder

```
cd backend
```

#### Install dependencies from requirements.txt
```
pip install -r requirements.txt
```

#### Make migrations, load base data
Linux/MacOS:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py load -i -t
python3 manage.py createsuperuser --noinput
```
Windows:
```
python manage.py makemigrations
python manage.py migrate
python manage.py load -i -t
python manage.py createsuperuser --noinput
```

#### Run server
Linux/MacOS:
```
python3 manage.py runserver
```
Windows:
```
python manage.py runserver
```

#### Change proxy pass
- Go to frontend folder
```
cd ../frontend
```

- Change package.json, set
```
"proxy": "http://127.0.0.1:8000/"
```

#### Run frontend app
```
npm i
npm start
```

### Run by docker on local mashine

#### Make and fill .env file (You might use .env.dist as template)
Windows:
```
echo '' > .env
```

Linux:
```
touch .env
```

#### Go to the infra folder
```
cd ./infra
```

#### Start docker compose
```
docker compose up
```

#### Make migrations
```
docker compose exec backend python manage.py migrate
```

#### load base data
```
docker compose exec backend python manage.py createsuperuser --noinput
docker compose exec backend python manage.py load -t -t
```


### Run by docker on the server

#### Make and fill .env file (You might use .env.dist as template)
Windows:
```
echo '' > .env
```
Linux:
```
touch .env
```

#### On the local mashine go to infra folder
```
cd projectpath/infra
```

#### Update docker-compose.producrion
- Change docker Hub profile data

#### Add secrets for CI/CD in your repository
- ```DOCKER_USERNAME``` - username on DockerHub
- ```DOCKER_PASSWORD``` - password on DockerHub
- ```SERVER_HOST``` - server ip adress
- ```SERVER_USERNAME``` - username on server
- ```SSH_KEY``` - openssh private key
- ```PASSPHRASE``` - Passphrase for private key
- ```TELEGRAM_ID``` - Telegram bot id
- ```TELEGRAM_BOT_TOKEN``` - Telegram bot token

#### On the server make and go to the project folder
```
cd
mkdir foodgram
cd foodgram
```

#### Copy docker compose and .env files

```
scp -i C:\\path\\to\\openssh\\private\\key\\file docker-compose.production.yml
USERNAME@ServerIP:/home/USERNAME/foodgram/docker-compose.production.yml
scp -i C:\\path\\to\\openssh\\private\\key\\file .env.dist
USERNAME@ServerIP:/home/USERNAME/foodgram/.env
```

Add nginx server, redirect all requests on port in docker-compose nginx service
(default `127.0.0.1:7000`)

#### After all, push for starting workflow
#### Worflow runs on push in 'main' brunch!
