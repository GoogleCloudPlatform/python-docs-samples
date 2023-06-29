# Connecting to Cloud SQL - mysql

This demo application can be used to connect to Cloud SQL in two different ways:

1. [The Cloud SQL Python Connector](https://github.com/GoogleCloudPlatform/cloud-sql-python-connector) (recommended)

2. [The Cloud SQL Auth Proxy](https://github.com/GoogleCloudPlatform/cloud-sql-proxy)

Using the Cloud SQL Python Connector library is recommended over the Cloud SQL Auth
Proxy as it provides all the same functionality and features but as a native
Python package. See [cloud-sql-python-connector package](https://pypi.org/project/cloud-sql-python-connector/).

## Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

1. Create a 2nd Gen Cloud SQL Instance by following these
[instructions](https://cloud.google.com/sql/docs/mysql/create-instance). Note the connection
string, database user, and database password that you create.

1. Create a database for your application by following these
[instructions](https://cloud.google.com/sql/docs/mysql/create-manage-databases). Note the database
name.

1. Create a service account with the 'Cloud SQL Client' permissions by following these
[instructions](https://cloud.google.com/sql/docs/mysql/connect-external-app#4_if_required_by_your_authentication_method_create_a_service_account).
Download a JSON key to use to authenticate your connection.

## Cloud SQL Python Connector Usage

### Run App Locally

To run the demo application locally using the Cloud SQL Python Connector, set
environment variables and install dependencies as shown below.

Note: The `INSTANCE_CONNECTION_NAME` for your instance can be found on the
**Overview** page for your instance in the
[Google Cloud console](https://console.cloud.google.com/sql) or by running
the following command:

```sh
gcloud sql instances describe <INSTANCE_NAME> --format='value(connectionName)'
```

#### Linux / Mac OS

Use these terminal commands to initialize environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service/account/key.json'
export INSTANCE_CONNECTION_NAME='<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>'
export DB_USER='<YOUR_DB_USER_NAME>'
export DB_PASS='<YOUR_DB_PASSWORD>'
export DB_NAME='<YOUR_DB_NAME>'
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

#### Windows/PowerShell

Use these PowerShell commands to initialize environment variables:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/key.json"
$env:INSTANCE_CONNECTION_NAME="<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>"
$env:DB_USER="<YOUR_DB_USER_NAME>"
$env:DB_PASS="<YOUR_DB_PASSWORD>"
$env:DB_NAME="<YOUR_DB_NAME>"
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

#### Install Dependencies

Next, install the requirements into a virtual environment:

```bash
virtualenv --python python3 env
source env/bin/activate
pip install -r requirements.txt
```

#### Test the Application

Finally, start the application:

```bash
python app.py
```

Navigate towards `http://127.0.0.1:8080` to verify your application is running correctly.

### Deploy to App Engine Standard

To run on GAE-Standard, create an App Engine project by following the setup with these
[instructions](https://cloud.google.com/appengine/docs/standard/python3/quickstart#before-you-begin).

Update `app.standard.yaml` with the correct values to pass the environment
variables into the runtime. Your `app.standard.yaml` file should look like this:

Note: If you want to connect to Cloud SQL over Private IP, add the additional
env variable `PRIVATE_IP: True` below.

```yaml
runtime: python310
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  INSTANCE_CONNECTION_NAME: <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>
  DB_USER: <YOUR_DB_USER_NAME>
  DB_PASS: <YOUR_DB_PASSWORD>
  DB_NAME: <YOUR_DB_NAME>
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Next, the following command will deploy the application to your Google Cloud project:

```bash
gcloud app deploy app.standard.yaml
```

### Deploy to App Engine Flexible

To run on GAE-Flexible, create an App Engine project by following the setup for these
[instructions](https://cloud.google.com/appengine/docs/flexible/python/quickstart#before-you-begin).

First, update `app.flexible.yaml` with the correct values to pass the environment
variables into the runtime. Your `app.flexible.yaml` file should look like this:

Note: If you want to connect to Cloud SQL over Private IP, add the additional
env variable `PRIVATE_IP: True` below.

```yaml
runtime: custom
env: flex
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  INSTANCE_CONNECTION_NAME: <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>
  DB_USER: <YOUR_DB_USER_NAME>
  DB_PASS: <YOUR_DB_PASSWORD>
  DB_NAME: <YOUR_DB_NAME>
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Next, the following command will deploy the application to your Google Cloud project:

```bash
gcloud app deploy app.flexible.yaml
```

### Deploy to Cloud Run

See the [Cloud Run documentation](https://cloud.google.com/sql/docs/mysql/connect-run)
for more details on connecting a Cloud Run service to Cloud SQL.

Note: If you want to connect to Cloud SQL over Private IP, add the additional
env variable `--set-env-vars PRIVATE_IP=True` and
flag `--vpc-connector <YOUR_VPC_CONNECTOR>` below.

```sh
gcloud run deploy cloud-sql-demo \
  --allow-unauthenticated \
  --set-env-vars INSTANCE_CONNECTION_NAME='<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>' \
  --set-env-vars DB_USER='<YOUR_DB_USER_NAME>' \
  --set-env-vars DB_PASS='<YOUR_DB_PASSWORD>' \
  --set-env-vars DB_NAME='<YOUR_DB_NAME>'
```

Navigate your browser to the URL output at the end of the deployment process
to view the demo app!

It is recommended to use the [Secret Manager integration](https://cloud.google.com/run/docs/configuring/secrets) for Cloud Run instead
of using environment variables for the SQL configuration. The service injects the SQL credentials from
Secret Manager at runtime via an environment variable.

Create secrets via the command line:

```sh
echo -n $INSTANCE_CONNECTION_NAME | \
    gcloud secrets create [INSTANCE_CONNECTION_NAME_SECRET] --data-file=-
```

Deploy the service to Cloud Run specifying the env var name and secret name:

```sh
gcloud run deploy cloud-sql-demo \
  --allow-unauthenticated \
  --update-secrets INSTANCE_CONNECTION_NAME=[INSTANCE_CONNECTION_NAME_SECRET]:latest,\
    DB_USER=[DB_USER_SECRET]:latest, \
    DB_PASS=[DB_PASS_SECRET]:latest, \
    DB_NAME=[DB_NAME_SECRET]:latest
```

### Deploy to Cloud Functions

To deploy the service to [Cloud Functions](https://cloud.google.com/functions/docs) run the following command:

Note: If you want to connect to Cloud SQL over Private IP, add the additional
env variable `--set-env-vars PRIVATE_IP=True` and
flag `--vpc-connector <YOUR_VPC_CONNECTOR>` below.

```sh
gcloud functions deploy votes --gen2 --runtime python310 --trigger-http \
  --allow-unauthenticated \
  --entry-point votes \
  --region <INSTANCE_REGION> \
  --set-env-vars INSTANCE_CONNECTION_NAME=<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME> \
  --set-env-vars DB_USER=$DB_USER \
  --set-env-vars DB_PASS=$DB_PASS \
  --set-env-vars DB_NAME=$DB_NAME
```

Take note of the URL output at the end of the deployment process to view your function!

## Cloud SQL Auth Proxy Usage

### Running locally

To run this application locally, download and install the `cloud-sql-proxy` by
following the instructions [here](https://cloud.google.com/sql/docs/mysql/sql-proxy#install).

Instructions are provided below for using the proxy with a TCP connection or a Unix Domain Socket.
On Linux or Mac OS you can use either option, but on Windows the proxy currently requires a TCP
connection.

#### Launch proxy with TCP

To run the sample locally with a TCP connection, set environment variables and launch the proxy as
shown below.

##### Linux / Mac OS

Use these terminal commands to initialize environment variables:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service/account/key.json'
export INSTANCE_HOST='127.0.0.1'
export DB_PORT='3306'
export DB_USER='<YOUR_DB_USER_NAME>'
export DB_PASS='<YOUR_DB_PASSWORD>'
export DB_NAME='<YOUR_DB_NAME>'
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then use this command to launch the proxy in the background:

```bash
./cloud-sql-proxy <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME> &
```

##### Windows/PowerShell

Use these PowerShell commands to initialize environment variables:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/key.json"
$env:INSTANCE_HOST="127.0.0.1"
$env:DB_PORT="3306"
$env:DB_USER="<YOUR_DB_USER_NAME>"
$env:DB_PASS="<YOUR_DB_PASSWORD>"
$env:DB_NAME="<YOUR_DB_NAME>"
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then use this command to launch the proxy in a separate PowerShell session:

```powershell
Start-Process -filepath "C:\<path to proxy exe>" -ArgumentList "<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>"
```

#### Launch proxy with Unix Domain Socket

NOTE: this option is currently only supported on Linux and Mac OS. Windows users should use the
[Launch proxy with TCP](#launch-proxy-with-tcp) option.

To use a Unix socket, you'll need to create a directory and give write access to the user running
the proxy. For example:

```bash
sudo mkdir /cloudsql
sudo chown -R $USER /cloudsql
```

Use these terminal commands to initialize other environment variables as well:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service/account/key.json'
export INSTANCE_UNIX_SOCKET='/cloudsql/<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>'
export DB_USER='<YOUR_DB_USER_NAME>'
export DB_PASS='<YOUR_DB_PASSWORD>'
export DB_NAME='<YOUR_DB_NAME>'
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then use this command to launch the proxy in the background:

```bash
./cloud-sql-proxy --unix-socket /cloudsql <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME> &
```

#### Testing the application

Next, setup install the requirements into a virtual environment:

```bash
virtualenv --python python3 env
source env/bin/activate
pip install -r requirements.txt
```

Finally, start the application:

```bash
python app.py
```

Navigate towards `http://127.0.0.1:8080` to verify your application is running correctly.

### Deploy to App Engine Standard

To run on GAE-Standard, create an App Engine project by following the setup for these
[instructions](https://cloud.google.com/appengine/docs/standard/python3/quickstart#before-you-begin).

First, update `app.standard.yaml` with the correct values to pass the environment
variables into the runtime. Your `app.standard.yaml` file should look like this:

```yaml
runtime: python37
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  INSTANCE_UNIX_SOCKET: /cloudsql/<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>
  DB_USER: <YOUR_DB_USER_NAME>
  DB_PASS: <YOUR_DB_PASSWORD>
  DB_NAME: <YOUR_DB_NAME>
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Next, the following command will deploy the application to your Google Cloud project:

```bash
gcloud app deploy app.standard.yaml
```

### Deploy to App Engine Flexible

To run on GAE-Flexible, create an App Engine project by following the setup for these
[instructions](https://cloud.google.com/appengine/docs/flexible/python/quickstart#before-you-begin).

First, update `app.flexible.yaml` with the correct values to pass the environment
variables into the runtime. Your `app.flexible.yaml` file should look like this:

```yaml
runtime: custom
env: flex
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  INSTANCE_UNIX_SOCKET: /cloudsql/<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>
  DB_USER: <YOUR_DB_USER_NAME>
  DB_PASS: <YOUR_DB_PASSWORD>
  DB_NAME: <YOUR_DB_NAME>

beta_settings:
  cloud_sql_instances: <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Next, the following command will deploy the application to your Google Cloud project:

```bash
gcloud app deploy app.flexible.yaml
```

### Deploy to Cloud Run

See the [Cloud Run documentation](https://cloud.google.com/sql/docs/mysql/connect-run)
for more details on connecting a Cloud Run service to Cloud SQL.

```sh
gcloud run deploy cloud-sql-demo \
  --add-cloudsql-instances '<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>' \
  --set-env-vars INSTANCE_UNIX_SOCKET='/cloudsql/<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME>' \
  --set-env-vars DB_USER='<YOUR_DB_USER_NAME>' \
  --set-env-vars DB_PASS='<YOUR_DB_PASSWORD>' \
  --set-env-vars DB_NAME='<YOUR_DB_NAME>'
```

Navigate your browser to the URL output at the end of the deployment process
to view the demo app!

It is recommended to use the [Secret Manager integration](https://cloud.google.com/run/docs/configuring/secrets) for Cloud Run instead
of using environment variables for the SQL configuration. The service injects the SQL credentials from
Secret Manager at runtime via an environment variable.

Create secrets via the command line:

```sh
echo -n $INSTANCE_UNIX_SOCKET | \
    gcloud secrets create [INSTANCE_UNIX_SOCKET_SECRET] --data-file=-
```

Deploy the service to Cloud Run specifying the env var name and secret name:

```sh
gcloud run deploy cloud-sql-demo \
  --add-cloudsql-instances <PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME> \
  --update-secrets INSTANCE_UNIX_SOCKET=[INSTANCE_UNIX_SOCKET_SECRET]:latest,\
    DB_USER=[DB_USER_SECRET]:latest, \
    DB_PASS=[DB_PASS_SECRET]:latest, \
    DB_NAME=[DB_NAME_SECRET]:latest
```

### Deploy to Cloud Functions

To deploy the service to [Cloud Functions](https://cloud.google.com/functions/docs) run the following command:

```sh
gcloud functions deploy votes --gen2 --runtime python310 --trigger-http \
  --allow-unauthenticated \
  --entry-point votes \
  --region <INSTANCE-REGION> \
  --set-env-vars INSTANCE_UNIX_SOCKET=/cloudsql/<PROJECT_ID>:<INSTANCE_REGION>:<INSTANCE_NAME> \
  --set-env-vars DB_USER=$DB_USER \
  --set-env-vars DB_PASS=$DB_PASS \
  --set-env-vars DB_NAME=$DB_NAME
```

Take note of the URL output at the end of the deployment process to view your function!
