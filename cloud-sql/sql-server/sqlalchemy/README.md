# Connecting to Cloud SQL - SQL Server

## Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and 
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

2. Create a 2nd Gen Cloud SQL Instance by following these 
[instructions](https://cloud.google.com/sql/docs/sqlserver/create-instance). Note the connection string,
database user, and database password that you create.

3. Create a database for your application by following these 
[instructions](https://cloud.google.com/sql/docs/sqlserver/create-manage-databases). Note the database
name. 

4. Create a service account with the 'Cloud SQL Client' permissions by following these 
[instructions](https://cloud.google.com/sql/docs/sqlserver/connect-external-app#4_if_required_by_your_authentication_method_create_a_service_account).
Download a JSON key to use to authenticate your connection. 

## Running locally

To run this application locally, download and install the `cloud_sql_proxy` by
following the instructions [here](https://cloud.google.com/sql/docs/sqlserver/sql-proxy#install). 

### Launch proxy with TCP

To run the sample locally with a TCP connection, set environment variables and launch the proxy as
shown below.

### Linux / MacOS
Use these terminal commands to initialize environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/key.json
export INSTANCE_HOST='127.0.0.1'
export DB_PORT='1433'
export DB_USER='<YOUD_DB_USER_NAME>'
export DB_PASS='<YOUR_DB_PASSWORD>'
export DB_NAME='<YOUR_DB_NAME>'
```
Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then, use the following command to start the proxy in the background using TCP:
```bash
./cloud_sql_proxy -instances=<PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>=tcp:1433 -credential_file=$GOOGLE_APPLICATION_CREDENTIALS &
```

### Windows / PowerShell
Use these PowerShell commands to initialize environment variables:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/key.json"
$env:INSTANCE_HOST="127.0.0.1"
$env:DB_PORT="1433"
$env:DB_USER="<YOUR_DB_USER_NAME>"
$env:DB_PASS="<YOUR_DB_PASSWORD>"
$env:DB_NAME="<YOUR_DB_NAME"
```
Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then use this command to launch the proxy in a separate PowerShell session:
```powershell
Start-Process -filepath "C:\<path to proxy exe>" -ArgumentList "-instances=<PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>=tcp:1433 -credential_file=/path/to/service/account/key.json"
```

### Testing the application

Next, setup a virtual environment and install the application's requirements:
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

## Deploy to App Engine Standard

To run on GAE-Standard, create an App Engine project by following the setup for these 
[instructions](https://cloud.google.com/appengine/docs/standard/python3/quickstart#before-you-begin).

First, update `app.standard.yaml` with the correct values to pass the environment 
variables into the runtime. Your `app.standard.yaml` file should look like this:

```yaml
runtime: python37
entrypoint: gunicorn -b :$PORT app:app
env_variables:
  INSTANCE_CONNECTION_NAME: <PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>
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

## Deploy to App Engine Flexible

To run on GAE-Flexible, create an App Engine project by following the setup for these 
[instructions](https://cloud.google.com/appengine/docs/flexible/python/quickstart#before-you-begin).

First, update `app.flexible.yaml` with the correct values to pass the environment 
variables into the runtime. Your `app.flexible.yaml` file should look like this:

```yaml
runtime: custom
env: flex
entrypoint: gunicorn -b :$PORT app:app
env_variables:
  INSTANCE_HOST: '172.17.0.1'
  DB_PORT: '1433'
  DB_USER: <YOUR_DB_USER_NAME>
  DB_PASS: <YOUR_DB_PASSWORD>
  DB_NAME: <YOUR_DB_NAME>
beta_settings:
  cloud_sql_instances: <PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>=tcp:1433
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Next, the following command will deploy the application to your Google Cloud project:

```bash
gcloud app deploy app.flexible.yaml
```

## Deploy to Cloud Run

See the [Cloud Run documentation](https://cloud.google.com/sql/docs/sqlserver/connect-run)
for more details on connecting a Cloud Run service to Cloud SQL.

1. Build the container image:

```sh
gcloud builds submit --tag gcr.io/<YOUR_PROJECT_ID>/run-sqlserver
```

2. Deploy the service to Cloud Run:

```sh
gcloud run deploy run-sqlserver --image gcr.io/<YOUR_PROJECT_ID>/run-sqlserver \
  --add-cloudsql-instances '<PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>' \
  --set-env-vars INSTANCE_CONNECTION_NAME='<PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME>' \
  --set-env-vars DB_USER='<YOUR_DB_USER_NAME>' \
  --set-env-vars DB_PASS='<YOUR_DB_PASSWORD>' \
  --set-env-vars DB_NAME='<YOUR_DB_NAME>'
```

Take note of the URL output at the end of the deployment process.

Replace environment variables with the correct values for your Cloud SQL
instance configuration.

It is recommended to use the [Secret Manager integration](https://cloud.google.com/run/docs/configuring/secrets) for Cloud Run instead
of using environment variables for the SQL configuration. The service injects the SQL credentials from
Secret Manager at runtime via an environment variable.

Create secrets via the command line:
```sh
echo -n $DB_PASS | \
    gcloud secrets create [DB_PASS_SECRET] --data-file=-
```

Deploy the service to Cloud Run specifying the env var name and secret name:
```sh
gcloud beta run deploy SERVICE --image gcr.io/<YOUR_PROJECT_ID>/run-sql \
    --add-cloudsql-instances <PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME> \
    --update-secrets INSTANCE_CONNECTION_NAME=[INSTANCE_CONNECTION_NAME_SECRET]:latest, \
      DB_PORT-[DB_PORT_SECRET]:latest, \
      DB_USER=[DB_USER_SECRET]:latest, \
      DB_PASS=[DB_PASS_SECRET]:latest, \
      DB_NAME=[DB_NAME_SECRET]:latest
```

3. Navigate your browser to the URL noted in step 2.

For more details about using Cloud Run see http://cloud.run.
Review other [Python on Cloud Run samples](../../../run/).

## Deploy to Cloud Functions

To deploy the service to [Cloud Functions](https://cloud.google.com/functions/docs) run the following command:

```sh
gcloud functions deploy votes --runtime python39 --trigger-http --allow-unauthenticated \
--set-env-vars INSTANCE_CONNECTION_NAME=<PROJECT-ID>:<INSTANCE-REGION>:<INSTANCE-NAME> \
--set-env-vars DB_USER=$DB_USER \
--set-env-vars DB_PASS=$DB_PASS \
--set-env-vars DB_NAME=$DB_NAME
```

Take note of the URL output at the end of the deployment process or run the following to view your function:

```sh
gcloud app browse
```
