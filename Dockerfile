FROM python:3.7.3-alpine3.8
# FROM python:3.8.6

LABEL author='knoort'

# --- for alpine ---

RUN apk update && apk upgrade

RUN apk add --no-cache build-base

RUN pip3 install asyncpg

RUN apk add --update py3-pip postgresql-dev gcc python3-dev musl-dev  \
	jpeg-dev zlib-dev && pip install --upgrade pip 

# --- end alpine build ---

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

ENTRYPOINT [ "sh", "entrypoint.sh" ]

#	libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev \
#	build-essential  libssl-dev libffi-dev libjpeg-dev libpq-dev  \
#	libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev	      \