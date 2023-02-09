FROM python:3.9-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev && \
    apk add chromium chromium-chromedriver

ENV PYTHONUNBUFFERED = 1
# upgrade pip
RUN pip install --upgrade pip

COPY ./requirements.txt  /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN chmod 755 entry.sh

RUN /usr/bin/crontab crontab.txt

CMD ["/app/entry.sh"]