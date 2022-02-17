FROM python:3.9.5-slim-buster as base

RUN apt-get update \
  && apt-get -y install gcc vim antiword git\
  && apt-get clean

# Set working directory for all following in container commands
WORKDIR /usr/src/api/

# Handle all necessary dependencies
RUN pip install --upgrade pip
COPY ./api/requirements.txt .
RUN pip install -r requirements.txt

# Container Environment Variables
ARG AZURE_KEY
ARG AZURE_ENDPOINT
ARG DEBUG
ARG UPLOAD_ACCESS_KEY
ARG UPLOAD_SECRET_KEY

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV AZURE_KEY ${AZURE_KEY}
ENV AZURE_ENDPOINT ${AZURE_ENDPOINT}
ENV CONTAINERIZED True
ENV DEBUG ${DEBUG}
ENV UPLOAD_ACCESS_KEY ${UPLOAD_ACCESS_KEY}
ENV UPLOAD_SECRET_KEY ${UPLOAD_SECRET_KEY}

# Install API
COPY ./api/ .

