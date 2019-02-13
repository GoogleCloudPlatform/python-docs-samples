
# BigQuery command-line tool

The BigQuery command-line tool is installed as part of the [Cloud SDK](https://cloud-dot-devsite.googleplex.com/sdk/docs/) and can be used to interact with BigQuery. When you use CLI commands in a notebook, the command must be prepended with a `!`.

## View available commands

To view the available commands for the BigQuery command-line tool, use the `help` command.


```python
!bq help
```

## Create a new dataset

A dataset is contained within a specific [project](https://cloud.google.com/bigquery/docs/projects). Datasets are top-level containers that are used to organize and control access to your [tables](https://cloud.google.com/bigquery/docs/tables) and [views](https://cloud.google.com/bigquery/docs/views). A table or view must belong to a dataset. You need to create at least one dataset before [loading data into BigQuery](https://cloud.google.com/bigquery/loading-data-into-bigquery).

First, name your new dataset:


```python
dataset_id = "your_new_dataset"
```

The following command creates a new dataset in the US using the ID defined above.

NOTE: In the examples in this notebook, the `dataset_id` variable is referenced in the commands using both `{}` and `$`. To avoid creating and using variables, replace these interpolated variables with literal values and remove the `{}` and `$` characters.


```python
!bq --location=US mk --dataset $dataset_id
```

The response should look like the following:

```
Dataset 'your-project-id:your_new_dataset' successfully created.
```

## List datasets

The following command lists all datasets in your default project.


```python
!bq ls
```

The response should look like the following:

```
           datasetId            
 ------------------------------ 
  your_new_dataset              
```

## Load data from a local file to a table

The following example demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Loading Data into BigQuery from a local data source](https://cloud.google.com/bigquery/docs/loading-data-local) in the BigQuery documentation.


```python
!bq \
    --location=US \
    load \
    --autodetect \
    --skip_leading_rows=1 \
    --source_format=CSV \
    {dataset_id}.us_states_local_file \
    'resources/us-states.csv'
```

## Load data from Cloud Storage to a table

The following example demonstrates how to load a local CSV file into a new table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Introduction to loading data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage) in the BigQuery documentation.


```python
!bq \
    --location=US \
    load \
    --autodetect \
    --skip_leading_rows=1 \
    --source_format=CSV \
    {dataset_id}.us_states_gcs \
    'gs://cloud-samples-data/bigquery/us-states/us-states.csv'
```

## Run a query

The BigQuery command-line tool has a `query` command for running queries, but it is recommended to use the [magic command](./BigQuery%20Query%20Magic.ipynb) for this purpose.

## Cleaning Up

The following code deletes the dataset created for this tutorial, including all tables in the dataset.


```python
!bq rm -r -f --dataset $dataset_id
```
