ARG PYTHON_VERSION=3.9
FROM docker.arvancloud.ir/python:${PYTHON_VERSION}-slim as base

WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt && \
    pip install psycopg2-binary==2.9.9 gunicorn

# copy project
COPY . /app/
