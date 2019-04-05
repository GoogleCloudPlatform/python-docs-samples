FROM python:3.6.5-alpine

WORKDIR /app

RUN apk add --update build-base

ENV PATH /root/.local/bin:$PATH
ENV QUERIES_CRON_EXPRESSION '* * * * *'
ENV SUBSCRIPTION_NAME 'projects/gcp_proj_id/subscriptions/subscription_id'
ENV QB_BACK_URL_PROTOCOL 'http'
ENV QB_BACK_URL_HOST 'localhost'
ENV QB_BACK_URL_PORT '8080'
ENV PUBSUB_CREDENTIALS 'service_account'

COPY ./Pipfile.lock /app/

RUN pip3 install --upgrade pip \
    && pip3 install --user pipenv

RUN pipenv install --ignore-pipfile

COPY . /app/

CMD pipenv run python run.py