# Composer Migrate script

This document describes usage of composer_migrate.py script.

The purpose of the script is to provide a tool to migrate Composer 2 environments to Composer 3. The script performs side-by-side migration using save/load snapshots operations. The script performs the following steps:

1. Obtains the configuration of the source Composer 2 environment.
2. Creates Composer 3 environment with the corresponding configuration.
3. Pauses all dags in the source Composer 2 environment.
4. Saves a snapshot of the source Composer 2 environment.
5. Loads the snapshot to the target the Composer 3 environment.
6. Unpauses the dags in the target Composer 3 environment (only dags that were unpaused in the source Composer 2 environment will be unpaused).


## Prerequisites
1.  [Make sure you are authorized](https://cloud.google.com/sdk/gcloud/reference/auth/login) through `gcloud auth login` before invoking the script . The script requires [permissions to access the Composer environment](https://cloud.google.com/composer/docs/how-to/access-control).

1.  The script depends on [Python](https://www.python.org/downloads/) 3.8 (or newer), [gcloud](https://cloud.google.com/sdk/docs/install) and [curl](https://curl.se/). Make sure you have all those tools installed.

1.  Make sure that your Composer environment that you want to migrate is healthy. Refer to [this documentation](https://cloud.google.com/composer/docs/monitoring-dashboard) for more information specific signals indicating good "Environment health" and "Database health". If your environment is not healthy, fix the environment before running this script.

## Limitations
1.  Only Composer 2 environments can be migrated with the script.

1. The Composer 3 environment will be created in the same project and region as the Composer 2 environment.

1. Airflow version of the Composer 3 environment can't be lower than the Airflow version of the source Composer 2 environment.

1.  The script currently does not have any error handling mechanism in case of
    failure in running gcloud commands.

1.  The script currently does not perform any validation before attempting migration. If e.g. Airflow configuration of the Composer 2 environment is not supported in Composer 3, the script will fail when loading the snapshot.

1. Dags are paused by the script one by one, so with environments containing large number of dags it is advised to pause them manually before running the script as this step can take a long time.

1. Workloads configuration of created Composer 3 environment might slightly differ from the configuration of Composer 2 environment. The script attempts to create an environment with the most similar configuration with values rounded up to the nearest allowed value.

## Usage

### Dry run
Script executed in dry run mode will only print the configuration of the Composer 3 environment that would be created.
```
python3 composer_migrate.py \
    --project [PROJECT NAME] \
    --location [REGION] \
    --source_environment [SOURCE ENVIRONMENT NAME] \
    --target_environment [TARGET ENVIRONMENT NAME] \
    --target_airflow_version [TARGET AIRFLOW VERSION] \
    --dry_run
```

Example:

```
python3 composer_migrate.py \
    --project my-project \
    --location us-central1 \
    --source_environment my-composer-2-environment \
    --target_environment my-composer-3-environment \
    --target_airflow_version 2.10.2 \
    --dry_run
```

### Migrate
```
python3 composer_migrate.py \
    --project [PROJECT NAME] \
    --location [REGION] \
    --source_environment [SOURCE ENVIRONMENT NAME] \
    --target_environment [TARGET ENVIRONMENT NAME] \
    --target_airflow_version [TARGET AIRFLOW VERSION]
```

Example:

```
python3 composer_migrate.py \
    --project my-project \
    --location us-central1 \
    --source_environment my-composer-2-environment \
    --target_environment my-composer-3-environment \
    --target_airflow_version 2.10.2
```

## Troubleshooting

1.  Make sure that all prerequisites are met - you have the right permissions and tools, you are authorized and the environment is healthy.

1.  Follow up with [support channels](https://cloud.google.com/composer/docs/getting-support) if you need additional help. When contacting Google Cloud Support, make sure to provide all relevant information including complete output from this script.
