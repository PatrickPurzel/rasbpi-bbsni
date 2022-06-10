FROM python:alpine3.16
#
#DEV - ENV
#FROM woahbase/alpine-rpigpio:armv7l
#
ENV TZ=Europe/Berlin

ARG PUID=1001
ARG PGID=1001
#
RUN mkdir -p /opt/app

COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN set -xe \
    && apk add --update --no-cache -Uu --virtual .build-dependencies libffi-dev openssl-dev build-base musl \
    && pip3 install --no-cache -r requirements.txt\
    && apk del --purge .build-dependencies \
    && apk add --no-cache --purge curl ca-certificates musl wiringpi \
    && rm -rf /var/cache/apk/* /tmp/*
#
COPY test-connector.py /opt/app/test-connector.py
#
CMD ["python3", "./test-connector.py"]