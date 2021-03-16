FROM python:3.8

RUN mkdir /app
WORKDIR /app
ENV PORT=8000

RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD gunicorn funnyp.wsgi:application --bind 0.0.0.0:$PORT