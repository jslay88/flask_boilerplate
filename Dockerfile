FROM python:3-alpine as base

FROM base as builder
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install --prefix=/install --no-warn-script-location -r requirements.txt
RUN pip install --prefix=/install --no-warn-script-location uwsgi

FROM base
ENV POSTGRES_HOST postgres
ENV POSTGRES_PORT 5432
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres
WORKDIR /app

RUN apk --no-cache add postgresql-dev postgresql-client
COPY --from=builder /install /usr/local
COPY app app
COPY migrations migrations
COPY manage.py manage.py
COPY run.py run.py

COPY migrate.sh migrate
COPY run.sh run
RUN chmod +x migrate
RUN chmod +x run

RUN adduser -D flask
RUN chown -R flask:flask /app

USER flask
EXPOSE 5000
CMD ["./run"]
