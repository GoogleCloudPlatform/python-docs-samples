# Connecting to Cloud SQL - SQL Server

## Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and 
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

1. [Create a Google Cloud SQL "SQL Server" instance](
    https://console.cloud.google.com/sql/choose-instance-engine).

6.  Under the instance's "USERS" tab, create a new user. Note the "User name" and "Password".

7.  Create a new database in your Google Cloud SQL instance.
    
    1.  List your database instances in [Cloud Cloud Console](
        https://console.cloud.google.com/sql/instances/).
    
    2.  Click your Instance Id to see Instance details.

    3.  Click DATABASES.

    4.  Click **Create database**.

    2.  For **Database name**, enter `votes`.

    3.  Click **CREATE**.



1. Create a service account with the 'Cloud SQL Client' permissions by following these 
[instructions](https://cloud.google.com/sql/docs/postgres/connect-external-app#4_if_required_by_your_authentication_method_create_a_service_account).
Download a JSON key to use to authenticate your connection. 

## Running locally
To run this application locally, download and install the `cloud_sql_proxy` by
following the instructions [here](https://cloud.google.com/sql/docs/mysql/sql-proxy#install). 

### Linux / MacOS
Use these terminal commands to initialize environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/key.json
export CLOUD_SQL_CONNECTION_NAME='<MY-PROJECT>:<INSTANCE-REGION>:<INSTANCE-NAME>'
export DB_USER='my-db-user'
export DB_PASS='my-db-pass'
export DB_NAME='my_db'
export DB_HOST='127.0.0.1:1433'
```
Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then, use the following command to start the proxy in the background using TCP:
```bash
./cloud_sql_proxy -instances=${CLOUD_SQL_CONNECTION_NAME}=tcp:1433 sqlserver -u ${DB_USER} --host 127.0.0.1 &
```

### Windows / PowerShell
Use these PowerShell commands to initialize environment variables:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="<CREDENTIALS_JSON_FILE>"
$env:CLOUD_SQL_CONNECTION_NAME="<MY-PROJECT>:<INSTANCE-REGION>:<INSTANCE-NAME>"
$env:DB_USER="my-db-user"
$env:DB_PASS="my-db-pass"
$env:DB_NAME="my_db"
$env:DB_HOST="127.0.0.1:1433"
```
Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/overview) to
help keep secrets safe.

Then use this command to launch the proxy in a separate PowerShell session:
```powershell
Start-Process -filepath "C:\<path to proxy exe>" -ArgumentList "-instances=<MY-PROJECT>:<INSTANCE-REGION>:<INSTANCE-NAME>=tcp:1433 -credential_file=<CREDENTIALS_JSON_FILE>"
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
python main.py
```

Navigate towards `http://127.0.0.1:8080` to verify your application is running correctly.

## Deploy to App Engine Flexible

App Engine Flexible supports connecting to your SQL Server instance through TCP

First, update `app.yaml` with the correct values to pass the environment 
variables and instance name into the runtime.

Then, make sure that the service account `service-{PROJECT_NUMBER}>@gae-api-prod.google.com.iam.gserviceaccount.com` has the IAM role `Cloud SQL Client`.

Next, the following command will deploy the application to your Google Cloud project:
```bash
gcloud beta app deploy
```

