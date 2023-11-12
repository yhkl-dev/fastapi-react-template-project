# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
# COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./pyproject.toml /usr/src/app/pyproject.toml
RUN poetry config virtualenvs.create false
# RUN pip install -r requirements.txt --no-cache-dir --no-build-isolation
RUN poetry install

# copy project
COPY . /usr/src/app/

RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]