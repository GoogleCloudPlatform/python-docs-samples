# Workaround for google-api-core Python 3.11 Deprecation Warning

This tool provides a workaround for Cloud Composer environments running Python 3.11 where `google-api-core` triggers high DAG parsing times, elevated worker CPU usage, or deprecation log spam.

## When to Use This

Use this workaround if:
- Your Cloud Composer environment is running on Python 3.11.
- You see `FutureWarning` logs from `google.api_core._python_version_support` indicating that Python 3.11 will reach end of life.
- You notice increased DAG parsing latency or worker CPU usage after entering the 365-day Python 3.11 EOL window (October 2026).

### Root Cause
`google-api-core` emits a deprecation warning starting 365 days before a Python version reaches community EOL. While emitting this warning, it calls `importlib.metadata.packages_distributions()`, which scans all installed packages across `site-packages` on disk. In Cloud Composer, where DAG processors and workers frequently spawn fresh Python subprocesses, repeated filesystem metadata scans cause measurable parse latency and CPU overhead.

## What the Workaround Does

`sitecustomize.py` is an import hook that CPython runs automatically on startup before user code executes. This script:
1. Changes `DEPRECATION_WARNING_PERIOD` from 365 days to 60 days, deferring the warning until August 2027.
2. Stubs `_get_pypi_package_name` to return `None`, preventing `packages_distributions()` from scanning disk.
3. Cleans up its own folder from `sys.path` immediately after load so subsequent imports do not re-scan the patch directory.

Because the file contains no DAG objects and avoids DAG-related keywords, Airflow's default `dag_discovery_safe_mode = True` ignores it during DAG parsing.

## How to Apply

### Step 1: Upload `sitecustomize.py` to GCS

Copy `sitecustomize.py` to a `patches/` directory in your environment's DAGs bucket:

```bash
gcloud storage cp sitecustomize.py gs://<YOUR_DAGS_BUCKET>/dags/patches/sitecustomize.py
```

You can find your DAGs bucket name by running:
```bash
gcloud composer environments describe <ENVIRONMENT_NAME> \
    --location <LOCATION> \
    --format="value(config.dagGcsPrefix)"
```

### Step 2: Set the `PYTHONPATH` Environment Variable

Add the patch folder to `PYTHONPATH` on your Composer environment:

```bash
gcloud composer environments update <ENVIRONMENT_NAME> \
    --location <LOCATION> \
    --update-env-variables PYTHONPATH=/home/airflow/gcs/dags/patches
```

> **Important:** If your environment already defines a custom `PYTHONPATH`, preserve your existing paths by separating them with a colon (`:`):
> ```bash
> --update-env-variables PYTHONPATH=/home/airflow/gcs/dags/patches:<EXISTING_PATH>
> ```

This update triggers a rolling restart of Composer workloads. Once restarted, all Python subprocesses (scheduler, workers, DAG processor) will load `sitecustomize.py` on startup.

### Note on `dag_discovery_safe_mode`

If you explicitly disabled safe mode (`[core] dag_discovery_safe_mode = False`), add `patches/*` to your `dags/.airflowignore` file to prevent the DAG file processor from attempting to parse the patch directory:

```text
patches/*
```

## Verification

After the environment finishes updating:
1. Check Cloud Logging or task logs in the Airflow UI. The `_python_version_support` `FutureWarning` messages should stop appearing.
2. In the Cloud Monitoring dashboard for Composer, check the **DAG Processing: Total Parse Time** metric. Parse times should return to baseline levels.

## How to Remove

Once your environment is upgraded to a Composer image or `google-api-core` version with the upstream fix, remove the workaround:

1. Remove `PYTHONPATH` (or restore your original value):
   ```bash
   gcloud composer environments update <ENVIRONMENT_NAME> \
       --location <LOCATION> \
       --remove-env-variables PYTHONPATH
   ```

2. Delete the patch file from the bucket:
   ```bash
   gcloud storage rm gs://<YOUR_DAGS_BUCKET>/dags/patches/sitecustomize.py
   ```
