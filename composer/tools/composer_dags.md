# Composer DAGs Pausing/Unpausing script

This document describes usage of composer_dags.py script.

The purpose of the script is to provide a tool to pause or unpause all the DAGs 
(except airflow_monitoring) of a Composer environment.

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

1.  Supported environment versions: all Composer versions 

1.  The script depends on [Python](https://www.python.org/downloads/) 3.6 (or newer), [gcloud](https://cloud.google.com/sdk/docs/install) and [kubectl](https://kubernetes.io/docs/tasks/tools/). Make sure
    you have all those tools installed.

1.  Make sure that your Composer environment is healthy. Refer to
    [this documentation](https://cloud.google.com/composer/docs/monitoring-dashboard)
    for more information specific signals indicating good "Environment health" and
    "Database health". If your environment is not healthy, fix the environment before
    running this script.

## Limitations

1.  The script currently does not have any error handling mechanism in case of
    failure in running gcloud commands.

1.  The script does not perform any DAG validation after the operation.

## Usage

### Pause/Unpause all the DAGs in an environment

```
python3 composer_dags.py \
    --project [PROJECT NAME] \
    --environment [SOURCE ENVIRONMENT NAME] \
    --location [REGION] \
    --operation [OPERATION]
```

Example:

```
python3 composer_dags.py \
    --project my-project \
    --environment my-airflow-1-composer-environment \
    --location europe-west4 \
    --operation pause
```

```
python3 composer_dags.py \
    --project my-project \
    --environment my-airflow-1-composer-environment \
    --location europe-west4 \
    --operation unpause
```

## Troubleshooting

1.  Make sure that all prerequisites are met - you have the right permissions
    and tools, you are authorized and the environment is healthy.

1.  If the error seems to be related to required permissions, double check that
    you have permissions to
    [access the Composer environment and its GKE cluster](https://cloud.google.com/composer/docs/how-to/access-control).

1.  Follow up with [support channels](https://cloud.google.com/composer/docs/getting-support)
    if you need additional help. When contacting Google Cloud Support, make sure to provide
    all relevant information including complete output from this script.
