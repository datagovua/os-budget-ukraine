FROM python:3.5-alpine

RUN apk update && apk upgrade && \
    apk add tini alpine-sdk libxml2-dev libxslt-dev libgcrypt-dev && \
    pip install pyunpack && \
    pip install git+https://github.com/frictionlessdata/datapackage-pipelines.git && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/sbin/tini", "--"]

EXPOSE 5000
WORKDIR /src
