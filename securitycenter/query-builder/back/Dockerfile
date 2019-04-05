FROM python:3.6.5-alpine

WORKDIR /app

RUN apk add --update build-base

ENV PATH /root/.local/bin:$PATH
ENV APP_ENV production
ENV db_host cloudsqldbhost
ENV db_port cloudsqldbport
ENV db_type Mysql
ENV organization_id gcloudorg
ENV organization_display_name org_display_name
ENV project_id project_id
ENV QUERIES_RUN_TOPIC topic_name
ENV MARK_CLEAN_UP_TOPIC clean_up_topic_name
ENV PUBSUB_CREDENTIALS 'service_account'
ENV NOTIFIER_CREDENTIALS 'service_account'
ENV WORKERS 16
ENV WORKERS_TIMEOUT 18000
ENV BIND_ADRESS 0.0.0.0:8080
ENV SCC_SEARCH_TIMEOUT_SECONDS 18000
ENV SCC_REQUEST_POOL_SIZE 4

COPY scc-query-builder/back/Pipfile.lock /app/
COPY scc-client /app/scc-client

# fix import path
RUN sed -i 's#./../../scc-client#./scc-client#g' Pipfile.lock

RUN pip3 install --upgrade pip \
    && pip3 install --user pipenv

RUN pipenv install --ignore-pipfile

COPY scc-query-builder/back /app/

CMD pipenv run gunicorn \
    -b ${BIND_ADRESS} \
    -w ${WORKERS} \
    -t ${WORKERS_TIMEOUT} \
    --preload \
    run:APP