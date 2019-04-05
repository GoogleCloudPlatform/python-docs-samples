% SCC Tools: **Creator APP Development Guidance**
% Security Cloud Command Center Tools

\setcounter{section}{0}
\setcounter{secnumdepth}{10}
\newpage

# Application

This is the application to be deployed at Google App Engine Flexible Environment

## Setup

Make sure you are in the folder **appflex**

```bash
cd creator/appflex
```

Create a virtual environment to install the dependencies

```bash
virtualenv creator-tests
source creator-tests/bin/activate
```

Install the test lib

```bash
pip install pytest
pip install pytest-mock
```

Install the requirements

```bash
pip install -r requirements.txt
```

Make sure you you have the scc-client library within the appflex directory of the creator app, and then install it:

```bash
pip install -e scc-client
```

Set the default project

```bash
gcloud config set project <gae_project>
```

Login to your organization

```bash
gcloud auth application-default login
```

If applicable, export the namespace value according to your deployed application. Otherwise it will use the default one

```bash
export CREATOR_NAMESPACE=<your-datastore-namespace>
```

## Execution

```bash
# organization id
export organization_id=<your-organization-id>

# service account file with access to SCC
# https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key
export SCC_CLIENT_DEVELOPER_KEY=<api-key-at-gcp-console-credentials>
```

```bash
pytest tests/ -s
```
