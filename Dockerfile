FROM python:3.7.4-alpine as builder
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install uwsgi

FROM python:3.7.4-alpine
WORKDIR /app
RUN apk add postgresql-dev
COPY --from=builder /app /app
COPY app app
RUN mkdir migrations
COPY manage.py manage.py
COPY run.py run.py

COPY migrate.sh migrate
RUN chmod +x migrate

COPY run.sh run
RUN chmod +x run

RUN adduser -D flask
RUN chown -R flask:flask /app

USER flask
EXPOSE 5000
CMD ["./run"]
