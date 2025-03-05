# Encrypting fields in Cloud SQL - MySQL with Tink

## Before you begin

1. If you haven't already, set up a Python Development Environment by following the [python setup guide](https://cloud.google.com/python/setup) and
[create a project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).

1. Create a 2nd Gen Cloud SQL Instance by following these
[instructions](https://cloud.google.com/sql/docs/sqlserver/create-instance). Note the connection string,
database user, and database password that you create.

1. Create a database for your application by following these
[instructions](https://cloud.google.com/sql/docs/sqlserver/create-manage-databases). Note the database
name.

1. Create a KMS key for your application by following these
[instructions](https://cloud.google.com/kms/docs/creating-keys). Copy the resource name of your
created key.

1. Grant an IAM user or service account the 'Cloud SQL Client' permissions by following these
[instructions](https://cloud.google.com/sql/docs/sqlserver/roles-and-permissions#introduction).

1. **macOS / Windows only**: Configure gRPC Root Certificates: On some platforms you may need to
accept the Google server certificates, see instructions for setting up
[root certs](https://github.com/googleapis/google-cloud-cpp/blob/main/google/cloud/bigtable/examples/README.md#configure-grpc-root-certificates).

## Running locally

Set up Application Default Credentials (ADC) for local development (using the
IAM user or service account who was granted the `Cloud SQL Client` role) by
following these [instructions](https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment).

To run this application locally, download and install the `cloud-sql-proxy` by
following the instructions
[here](https://cloud.google.com/sql/docs/sqlserver/connect-admin-proxy#install).

### Launch proxy with TCP

To run the sample locally with a TCP connection, set environment variables and launch the proxy as
shown below.

#### Linux / Mac OS

Use these terminal commands to initialize environment variables:

```bash
export DB_HOST='127.0.0.1:1433'
export DB_USER='<DB_USER_NAME>'
export DB_PASS='<DB_PASSWORD>'
export DB_NAME='<DB_NAME>'
export GCP_KMS_URI='<GCP_KMS_URI>'
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/quickstart) to
help keep secrets safe.

Then use this command to launch the proxy in the background:

```bash
./cloud-sql-proxy --port 1433 <project-id>:<region>:<instance-name> &
```

#### Windows/PowerShell

Use these PowerShell commands to initialize environment variables:

```powershell
$env:DB_HOST="127.0.0.1:1433"
$env:DB_USER="<DB_USER_NAME>"
$env:DB_PASS="<DB_PASSWORD>"
$env:DB_NAME="<DB_NAME>"
$env:GCP_KMS_URI='<GCP_KMS_URI>'
```

Note: Saving credentials in environment variables is convenient, but not secure - consider a more
secure solution such as [Secret Manager](https://cloud.google.com/secret-manager/docs/quickstart) to
help keep secrets safe.

Then use this command to launch the proxy in a separate PowerShell session:

```powershell
Start-Process -filepath "C:\<path to cloud-sql-proxy.exe>" -ArgumentList "--port 1433 <project-id>:<region>:<instance-name>"
```

### Install requirements

Next, setup install the requirements into a virtual environment:

```bash
virtualenv --python python3 env
source env/bin/activate
pip install -r requirements.txt
```

### Run the demo

Add new votes and view the collected votes:

```bash
python snippets/query_and_decrypt_data.py 
```
