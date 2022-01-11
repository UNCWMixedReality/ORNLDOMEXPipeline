FROM python:3.9.5-slim-buster

ARG AZURE_KEY
ARG AZURE_ENDPOINT

# Set working directory for all following in container commands
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AZURE_KEY ${AZURE_KEY}
ENV AZURE_ENDPOINT ${AZURE_ENDPOINT}

RUN apt-get update \
  && apt-get -y install gcc vim antiword \
  && apt-get clean

# Handle all necessary dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install App
COPY . .
