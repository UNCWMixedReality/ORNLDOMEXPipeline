FROM python:3.9.5-slim-buster as base

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
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

# Install App
COPY ./app/ .

# Change Work directory for API setup
WORKDIR /usr/src/api

# Copy new requirements
COPY ./api/requirements.txt .
RUN pip install -r requirements.txt

# Install API
COPY ./api/ .