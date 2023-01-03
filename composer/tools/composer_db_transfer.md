# Composer database transfer: Airflow 1.10.14/15 -> Airflow 2.0.1+

This document describes usage of composer_db_transfer.py script.

Purpose of the script it to provide a tool to migrate the metadata database,
DAGs, data and plugins from Composer environments with Airflow 1.10.14/15 to
existing Composer environment with Airflow 2.0.1+.

Dedicated tool is needed as in-place upgrade is not supported between those
versions.

## Deprecation notice

This script has been deprecated and will be removed in the future. "Snapshots"
are recommended tool to perform side-by-side upgrades of Cloud Composer
environments (https://cloud.google.com/composer/docs/save-load-snapshots).

## Prerequisites

1.  [Make sure you are authorized](https://cloud.google.com/sdk/gcloud/reference/auth/login)
    through `gcloud auth login` before invoking the script . The script requires
    [permissions to access the Composer environment](https://cloud.google.com/composer/docs/how-to/access-control)
    (roles/composer.environmentAndStorageObjectAdmin role is sufficient) and its
    GKE cluster (container.*).

1.  Make sure that you can access GKE cluster of Composer environment through
    kubectl (e.g. if you are not able to successfully execute
    `kubectl get pods`, the script will fail). "Unable to connect to the server:
    dial tcp [IP ADDRESS]:443: connect: connection timed out" reported by
    kubectl indicates that kubectl can not connect to GKE cluster.
    [Refer to the documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#cloud_shell)
    about setting up access to private GKE cluster if you have private IP environment.

1.  Supported source versions: all Composer versions with Airflow 1.10.14 or
    1.10.15

1.  Supported destination versions: all Composer versions with Airflow 2.0.1 and
    newer

1.  The script depends on Python 3.6 (or newer), gcloud and kubectl. Make sure
    you have all those tools installed.

1.  Make sure that your Composer environment is healthy. Refer to
    [this documentation](https://cloud.google.com/composer/docs/monitoring-dashboard)
    for more information specific signals indicating good "Environment health" and
    "Database health". If your environment is not healthy, fix the environment before
    running this script.

1.  Make sure that you have write access to the current directory. The script
    exports `KUBECONFIG` environment variable to store credentials to the
    Composer's GKE cluster in the current directory (on the machine that executes
    the script). The purpose is not to interfere with existing GKE-related
    user's configuration.

1.  Pause the DAGs before exporting the database.

## Limitations

1.  Logs from old DAG executions are not transferred (but history of executions
    in the database is transferred).

1.  The script does not perform any DAG modifications, does not validate that
    the DAGs are suitable to run in Airflow 2.0 and does not verify that
    suitable dependencies are installed in target environment. Airflow
    [upgrade_check](https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/upgrade-check.html)
    can be used to troubleshoot DAG compatibility issues.

1.  `dag_code` and `serialized_dag` tables are not synchronized directly.
    Database entries for imported DAGs are created by Airflow in the new
    environment.

1.  The script does not prevent DAGs from being scheduled in both old and new
    environment. This can be prevented by pausing the DAGs before exporting
    them and unpausing them in the new environment.

1.  Airflow web server in target environment might temporarily not be available
    after the database transfer (up to a couple of minutes).

1.  The environment might need some time to parse imported DAGs. As a result
    they might appear in the web UI with some delay (depending on a number and
    complexity of the DAGs).

1.  Import operation removes all records from the target environment. Files
    existing in the environment's bucket are not deleted.

1.  The script does not override gcloud configuration and exports it's own
    kubeconfig. Temporary files for GKE deployment and kubeconfig created in the
    working directory have unique names.

1.  File with fernet key created by export operation is not deleted by import
    operation.

## Usage

### Export from an old environment (Airflow 1.10.14/15)

As a result of export operation CSV files with exported database are stored as
/export/tables/[TABLE NAME].csv in the environment's bucket. DAGs, plugins and
data directories are stored in /export/dirs in the environment's bucket.

A file with a fernet key is going to be created on the machine executing the
script.

```
python3 composer_db_transfer.py export \
    --project [PROJECT NAME] \
    --environment [SOURCE ENVIRONMENT NAME] \
    --location [REGION] \
    --fernet-key-file [PATH TO FERNET KEY FILE - TO BE CREATED]
```

Example:

```
python3 composer_db_transfer.py export \
    --project my-project \
    --environment my-airflow-1-composer-environment \
    --location europe-west4 \
    --fernet-key-file my-fernet-key
```

### Copying the files between the environments

Exported files can be copied to the target environment, e.g. with:

```
gsutil -m cp -r gs://[SOURCE ENV BUCKET NAME]/export gs://[TARGET ENV BUCKET NAME]/import
```

Example:

```
gsutil -m cp -r gs://europe-west4-my-airflow-1-composer-environment-123456abc-bucket/export gs://europe-west4-my-airflow-2-composer-environment-789xyz-bucket/import
```

### Import to a new environment (Airflow 2.0.1+)

CSV files that should be imported are expected to be stored as
/import/tables/[TABLE NAME].csv in the environment's bucket. dags, plugins and
data directories that should be imported are expected to be stored in
/import/dirs in the environment's bucket.

`fernet-key-file` parameter specifies path to the fernet key file of the source
environment on the machine executing the script. It is created during export
phase.

```
python3 composer_db_transfer.py import \
    --project [PROJECT NAME] \
    --environment [TARGET ENVIRONMENT NAME] \
    --location [REGION] \
    --fernet-key-file [PATH TO FERNET KEY FILE FROM SOURCE ENVIRONMENT]
```

Example:

```
python3 composer_db_transfer.py import \
    --project my-project \
    --environment my-airflow-2-composer-environment \
    --location europe-west4 \
    --fernet-key-file my-fernet-key
```

## Troubleshooting

1.  Make sure that all prerequisites are met - you have the right permissions
    and tools, you are authorized and the environment is healthy.

1.  "Unable to connect to the server: dial tcp [IP ADDRESS]:443: connect:
    connection timed out" might indicate that network settings prevent kubectl
    from connecting to GKE cluster. This is especially likely if you have a
    private IP environment. In such a case additional configuration might be
    required. Check
    [the documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#cloud_shell)
    for more information.

1.  If the error seems to be related to required permissions, double check that
    you have permissions to
    [access the Composer environment and its GKE cluster](https://cloud.google.com/composer/docs/how-to/access-control).

1.  "HTTPError 403: The service account does not have the required permissions
    for the bucket" might indicate that imported data was not properly copied to
    the import "directory" in environment's bucket (may actually not exist at
    all).

1.  Exit code 137 reported from command executed in the GKE cluster might
    indicate that the relevant workload was terminated. Possibly the environment
    is not healthy.

1.  Follow up with [support channels](https://cloud.google.com/composer/docs/getting-support)
    if you need additional help. When contacting Google Cloud Support, make sure to provide
    all relevant information including complete output from this script.
