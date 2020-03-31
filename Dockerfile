FROM python:3.7

COPY ./requirements.txt /scrapy/requirements.txt

RUN pip install -r /scrapy/requirements.txt

RUN apt update

RUN apt install wait-for-it

COPY . /scrapy

WORKDIR /scrapy
