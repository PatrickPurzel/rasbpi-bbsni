FROM woahbase/alpine-rpigpio:armhf
#
ARG PUID=1001
ARG PGID=1001
#
RUN set -xe \
    && apk add --no-cache -Uu --virtual .build-dependencies python3-dev libffi-dev openssl-dev build-base musl \
    && pip3 install --no-cache --upgrade pyserial RPi.GPIO \
    && apk del --purge .build-dependencies \
    && apk add --no-cache --purge curl ca-certificates musl wiringpi \
    && rm -rf /var/cache/apk/* /tmp/*
#
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip3 install -r requirements.txt
COPY test-connector.py /opt/app/test-connector.py
#

# ENTRYPOINT ["/init"]
# ENTRYPOINT ["/usr/bin/python"]