# Query Builder Scheduler

The scheduler application will get the ids of the scheduled queries posted at PubSub, and in a 
configured scheduling iteration, call the endpoint of backend application to run the query

The following environment variables definition are required to execute the application:

* SUBSCRIPTION_NAME: expected in the format "projects/{project_id}/subscriptions/{subscription_id}"
* PUBSUB_CREDENTIALS: JSON content of the given service account

The following environment variables could be used to change default configurations:

* QUERIES_CRON_EXPRESSION: schedule cron expression
* QB_BACK_URL_PROTOCOL: backend application communication protocol
* QB_BACK_URL_HOST: backend application host
* QB_BACK_URL_PORT: backend application port

## Initial setup

### Pipenv setup

We recommend the use of [pipenv](https://github.com/pypa/pipenv) to run tests on isolated environment

```bash
pip install --user pipenv
```

### Dependencies installation

```bash
(cd scc-query-builder/scheduler/ && pipenv install --ignore-pipfile)
```

## Execute Application

```bash
(cd scc-query-builder/scheduler/ && pipenv run python)
```

