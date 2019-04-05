% SCC Tools: **SCC Client**
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# Requirements

Before start, make sure you've gone through the section **'How to install the tools'** in the main  **`README-${version}.pdf`** file delivered in this package. It contains **important pre-requisites and pre-installation instructions you must do** to proceed to the installation of this tool.

# Run tests

## Initial setup

To be able to run the tests you need to run the commands below

### Environment variables config

```bash
export SCC_SA_CLIENT_FILE=<your-service-account-file>
export organization_id=<your-org-id>
```

### Pipenv setup

We recommend the use of [pipenv](https://github.com/pypa/pipenv) to run tests on isolated environment

```bash
pip install --user pipenv
```

### Dependencies installation

```bash
(cd scc-client && pipenv install --ignore-pipfile --dev)
```

## Run all tests on application

```bash
(cd scc-client && pipenv run python -m coverage run --source client -m pytest -vvs tests -rs)
```

## How to run a specific test file

```bash
(cd scc-client && pipenv run python -m coverage run --source client -m pytest -vvs tests/${test_file} -rs)
```

## How to see coverage report

```bash
(cd scc-client && pipenv run python -m coverage report -m)
```

## Running tests for beta API

### Setup

In order to execute tests on beta API the following setup still needed:

* A valid service account named `cscc_api_client.json` at `scc-client/accounts`
* `SCC_CLIENT_DEVELOPER_KEY` environment variable set with expected value for API key that can be caught on SCC Beta Project on GCloud console (API & services > Credentials) 

This need to be done due to non-mocking on the discovery API step for SCC beta API  


### Execution

```bash
(cd scc-client && pipenv run python -m pytest -vvs tests/test_scc_client_beta.py -rs)
```