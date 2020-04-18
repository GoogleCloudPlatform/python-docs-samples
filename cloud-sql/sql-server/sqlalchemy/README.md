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

1. Install the version of [Microsoft ODBC 17 Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15_) for your operating system.

1. Create a service account with the 'Cloud SQL Client' permissions by following these 
[instructions](https://cloud.google.com/sql/docs/postgres/connect-external-app#4_if_required_by_your_authentication_method_create_a_service_account).
Download a JSON key to use to authenticate your connection. 

1. Use the information noted in the previous steps:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/key.json
export CLOUD_SQL_CONNECTION_NAME='<MY-PROJECT>:<INSTANCE-REGION>:<INSTANCE-NAME>'
export DB_USER='my-db-user'
export DB_PASS='my-db-pass'
export DB_NAME='my_db'
```
Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Cloud KMS](https://cloud.google.com/kms/) to help keep secrets safe.

## Running locally

To run this application locally, download and install the `cloud_sql_proxy` by
following the instructions [here](https://cloud.google.com/sql/docs/mysql/sql-proxy#install). 

Then, use the following command to start the proxy in the
background using TCP:
```bash
./cloud_sql_proxy -instances=${CLOUD_SQL_CONNECTION_NAME}=tcp:1433 sqlserver -u ${DB_USER} --host 127.0.0.1
```

Next, setup install the requirements into a virtual enviroment:
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

