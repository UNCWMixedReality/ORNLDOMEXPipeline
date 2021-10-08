FROM python:3.9.5-slim-buster

# Set working directory for all following in container commands
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install gcc vim \
  && apt-get clean

# Handle all necessary dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install App
COPY . .
