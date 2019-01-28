
# BigQuery command-line tool

The BigQuery command-line tool is installed as part of the [Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/), and can be used to interact with BigQuery using shell commands instead of Python code. Note that shell commands in a notebook must be prepended with a `!`.

## View available commands

To view the available commands for the BigQuery command-line tool, use the `--help` flag.


```python
!bq help
```

## Create a new dataset

A dataset is contained within a specific [project](https://cloud.google.com/bigquery/docs/projects). Datasets are top-level containers that are used to organize and control access to your [tables](https://cloud.google.com/bigquery/docs/tables) and [views](https://cloud.google.com/bigquery/docs/views). A table or view must belong to a dataset, so you need to create at least one dataset before [loading data into BigQuery](https://cloud.google.com/bigquery/loading-data-into-bigquery).

The command below creates a new dataset in the US named "your_new_dataset".


```python
!bq --location=US mk --dataset "your_dataset_id"
```

## List datasets

The command below lists lists all datasets in your current project.


```python
!bq ls
```

## Load data from a local file to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Loading Data into BigQuery from a Local Data Source](https://cloud.google.com/bigquery/docs/loading-data-local) in the BigQuery documentation.


```python
!bq --location=US load --autodetect --skip_leading_rows=1 --source_format=CSV your_dataset_id.us_states_local_file 'resources/us-states.csv'
```

## Load data from Google Cloud Storage to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Introduction to Loading Data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage) in the BigQuery documentation.


```python
!bq --location=US load --autodetect --skip_leading_rows=1 --source_format=CSV your_dataset_id.us_states_gcs 'gs://cloud-samples-data/bigquery/us-states/us-states.csv'
```

## Run a query

The BigQuery command-line tool has a `query` command for running queries, but it is recommended to use the [Magic command](./BigQuery%20Query%20Magic.ipynb) for this purpose.

## Cleaning Up

The following code deletes the dataset created for this tutorial, including all tables in the dataset.


```python
!bq rm -r -f --dataset your_dataset_id
```
