# Query Builder

## Run tests

### Initial setup

To be able to run the tests you need to run the commands below

#### Pipenv setup

We recommend the use of [pipenv](https://github.com/pypa/pipenv) to run tests on isolated environment

```bash
pip install --user pipenv
```

#### Variables setup

Add organization ID as an environment variable
```bash
export organization_id=<your-org-id>
```

If your test involve the pubsub service (`test_pubsub_service.py`), the following environment variables should also be set:
```bash
export PUBSUB_CREDENTIALS=$(cat some_service_account.json)
export NOTIFIER_CREDENTIALS=$(cat some_service_account.json)
```


#### Dependencies installation

```bash
(cd scc-query-builder/back/ && pipenv install --ignore-pipfile --dev)
```

### Run application on development mode

```bash
export SCC_CLIENT_DEVELOPER_KEY=<your-developer-key>
export SCC_SA_CLIENT_FILE=<service-account-key-file>
export SCC_SERVICE_ACCOUNT=<e-mail-service>
export organization_id=<your-organization-id>
(cd scc-query-builder/back/ && pipenv run python run.py)
```
It will set up a local Sqlite database

### Run all tests on application

```bash
export SCC_CLIENT_DEVELOPER_KEY=<your-developer-key>
export SCC_SA_CLIENT_FILE=<service-account-key-file>
export SCC_SERVICE_ACCOUNT=<e-mail-service>
export organization_id=<your-organization-id>
(cd scc-query-builder/back/ && pipenv run python -m coverage run --source query_builder -m pytest -vvs tests)
```

### How to run a specific test file

```bash
export SCC_CLIENT_DEVELOPER_KEY=<your-developer-key>
export SCC_SA_CLIENT_FILE=<service-account-key-file>
export SCC_SERVICE_ACCOUNT=<e-mail-service>
export organization_id=<your-organization-id>
(cd scc-query-builder/back/ && pipenv run python -m coverage run --source query_builder -m pytest -vvs ${test_file_path})
```

### How to see coverage report

```bash
(cd scc-query-builder/back/ && pipenv run python -m coverage report -m)
```

## Database

Sqlite is right now the default database
To use MySql export a enviroment variable for db_type

```bash
export SCC_CLIENT_DEVELOPER_KEY=<your-developer-key>
export SCC_SA_CLIENT_FILE=<service-account-key-file>
export SCC_SERVICE_ACCOUNT=<e-mail-service>
export organization_id=<your-organization-id>
(cd scc-query-builder/back/ && export db_type=mysql)
```
