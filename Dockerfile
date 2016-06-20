FROM python:2.7
# Dockerize for waiting on postgres being ready.
#  https://github.com/jwilder/dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.2.0/dockerize-linux-amd64-v0.2.0.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.2.0.tar.gz
RUN rm dockerize-linux-amd64-v0.2.0.tar.gz
# Setup Django.
RUN mkdir /app
ENV PYTHONUNBUFFERED 1
COPY . /app/
RUN pip install -r /app/requirements/dev.txt
#ENV SECRET_KEY=docker
ENV DJANGO_SETTINGS_MODULE=website.settings.dev
WORKDIR /app
