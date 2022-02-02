FROM python:3.8-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD . /app/

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/

RUN pip install -r requirements.txt && \
    pip3 install --upgrade pip  && \
    pip3 install pipenv

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn funnyp.wsgi:application --bind 0.0.0.0:8000