FROM python:3.7.3-alpine3.8

LABEL author='knoort'

RUN apk update && apk upgrade

RUN apk add --update py3-pip postgresql-dev gcc python3-dev musl-dev  \
	jpeg-dev zlib-dev && pip install --upgrade pip 

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

ENTRYPOINT [ "sh", "entrypoint.sh" ]
