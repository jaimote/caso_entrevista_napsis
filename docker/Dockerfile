FROM alpine:3.13
#FROM python:3.6-alpine
RUN apk add --no-cache g++ freetype-dev jpeg-dev zlib-dev
RUN apk add --no-cache alpine-sdk linux-headers libxml2-dev gcc musl-dev python3-dev libffi-dev openssl-dev

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN apk update && apk add --no-cache curl  wkhtmltopdf xvfb fontconfig freetype ttf-dejavu ttf-droid ttf-freefont ttf-liberation ttf-ubuntu-font-family libzbar py3-scipy

RUN apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f
    

RUN adduser -D userapi
USER userapi

COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt



EXPOSE 5000
CMD python3 manage.py runserver --host 0.0.0.0
