FROM python:3.6.5-alpine

WORKDIR /app

RUN apk add --update build-base

ENV PATH /root/.local/bin:$PATH
ENV APP_ENV production
ENV CLEAN_UUID_CRON_EXPRESSION '* * * * *'
ENV CLEAN_ALL_CRON_EXPRESSION '*/15 * * * *'
ENV SUBSCRIPTION_NAME 'projects/gcp_proj_id/subscriptions/subscription_id'
ENV PUBSUB_CREDENTIALS 'service_account'
ENV ORGANIZATION_ID 'organization_id'
ENV SCC_SEARCH_TIMEOUT_SECONDS 18000
ENV QPS 4

COPY scc-query-builder/cleanup/Pipfile.lock /app/
COPY scc-client /app/scc-client

# fix import path
RUN sed -i 's#./../../scc-client#./scc-client#g' Pipfile.lock

RUN pip3 install --upgrade pip \
    && pip3 install --user pipenv

RUN pipenv install --ignore-pipfile

COPY scc-query-builder/cleanup /app/

CMD pipenv run python run.py
