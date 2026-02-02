FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gettext \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Create project on first build
# RUN django-admin startproject comercial_map_api . && mv comercial_map_api/* . && rmdir comercial_map_api
