
# BigQuery basics

[BigQuery](https://cloud.google.com/bigquery/docs/) is a petabyte-scale analytics data warehouse that you can use to run SQL queries over vast amounts of data in near realtime. This page shows you how to get started with the Google BigQuery API using the Python client library.

## Import the libraries used in this tutorial


```python
from google.cloud import bigquery
import pandas
```

## Initialize a client

To use the BigQuery Python client library, start by initializing a client. The BigQuery client is used to send and receive messages from the BigQuery API.

### Client project
The `bigquery.Client` object uses your default project. Alternatively, you can specify a project in the `Client` constructor. For more information about how the default project is determined, see the [google-auth documentation](https://google-auth.readthedocs.io/en/latest/reference/google.auth.html).


### Client location
Locations are required for certain BigQuery operations such as creating a dataset. If a location is provided to the client when it is initialized, it will be the default location for jobs, datasets, and tables.

Run the following to create a client with your default project:


```python
client = bigquery.Client(location="US")
print("Client creating using default project: {}".format(client.project))
```

To explicitly specify a project when constructing the client, set the `project` parameter:


```python
# client = bigquery.Client(location="US", project="your-project-id")
```

## Run a query on a public dataset

The following example queries the BigQuery `usa_names` public dataset to find the 10 most popular names. `usa_names` is a Social Security Administration dataset that contains all names from Social Security card applications for births that occurred in the United States after 1879.

Use the [Client.query](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.query) method to run the query, and the [QueryJob.to_dataframe](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.QueryJob.html#google.cloud.bigquery.job.QueryJob.to_dataframe) method to return the results as a pandas [`DataFrame`](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).


```python
query = """
    SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
"""
query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
)  # API request - starts the query

df = query_job.to_dataframe()
df
```

## Run a parameterized query

BigQuery supports query parameters to help prevent [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) when you construct a query with user input. Query parameters are only available with [standard SQL syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/). Query parameters can be used as substitutes for arbitrary expressions. Parameters cannot be used as substitutes for identifiers, column names, table names, or other parts of the query.

To specify a parameter, use the `@` character followed by an [identifier](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#identifiers), such as `@param_name`. For example, the following query finds all the words in a specific Shakespeare corpus with counts that are at least the specified value.

For more information, see [Running parameterized queries](https://cloud.google.com/bigquery/docs/parameterized-queries) in the BigQuery documentation.


```python
# Define the query
sql = """
    SELECT word, word_count
    FROM `bigquery-public-data.samples.shakespeare`
    WHERE corpus = @corpus
    AND word_count &gt;= @min_word_count
    ORDER BY word_count DESC;
"""

# Define the parameter values in a query job configuration
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("corpus", "STRING", "romeoandjuliet"),
        bigquery.ScalarQueryParameter("min_word_count", "INT64", 250),
    ]
)

# Start the query job
query_job = client.query(sql, location="US", job_config=job_config)

# Return the results as a pandas DataFrame
query_job.to_dataframe()
```

## Create a new dataset

A dataset is contained within a specific [project](https://cloud.google.com/bigquery/docs/projects). Datasets are top-level containers that are used to organize and control access to your [tables](https://cloud.google.com/bigquery/docs/tables) and [views](https://cloud.google.com/bigquery/docs/views). A table or view must belong to a dataset. You need to create at least one dataset before [loading data into BigQuery](https://cloud.google.com/bigquery/loading-data-into-bigquery).


```python
# Define a name for the new dataset.
dataset_id = 'your_new_dataset'

# The project defaults to the Client's project if not specified.
dataset = client.create_dataset(dataset_id)  # API request
```

## Write query results to a destination table

For more information, see [Writing query results](https://cloud.google.com/bigquery/docs/writing-results) in the BigQuery documentation.


```python
sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""
table_ref = dataset.table("your_new_table_id")
job_config = bigquery.QueryJobConfig(
    destination=table_ref
)

# Start the query, passing in the extra configuration.
query_job = client.query(sql, location="US", job_config=job_config)

query_job.result()  # Waits for the query to finish
print("Query results loaded to table {}".format(table_ref.path))
```

## Load data from a pandas DataFrame to a new table


```python
records = [
    {"title": "The Meaning of Life", "release_year": 1983},
    {"title": "Monty Python and the Holy Grail", "release_year": 1975},
    {"title": "Life of Brian", "release_year": 1979},
    {"title": "And Now for Something Completely Different", "release_year": 1971},
]

# Optionally set explicit indices.
# If indices are not specified, a column will be created for the default
# indices created by pandas.
index = ["Q24980", "Q25043", "Q24953", "Q16403"]
df = pandas.DataFrame(records, index=pandas.Index(index, name="wikidata_id"))

table_ref = dataset.table("monty_python")
job = client.load_table_from_dataframe(df, table_ref, location="US")

job.result()  # Waits for table load to complete.
print("Loaded dataframe to {}".format(table_ref.path))
```

## Load data from a local file to a table

The following example demonstrates how to load a local CSV file into a new table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Loading Data into BigQuery from a local data source](https://cloud.google.com/bigquery/docs/loading-data-local) in the BigQuery documentation.


```python
source_filename = 'resources/us-states.csv'

table_ref = dataset.table('us_states_from_local_file')
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    autodetect=True
)

with open(source_filename, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)  # API request

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(
    job.output_rows, dataset_id, table_ref.path))
```

## Load data from Cloud Storage to a table

The following example demonstrates how to load a local CSV file into a new table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Introduction to loading data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage) in the BigQuery documentation.


```python
# Configure the load job
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV. The line below is optional.
    source_format=bigquery.SourceFormat.CSV
)
uri = 'gs://cloud-samples-data/bigquery/us-states/us-states.csv'
destination_table_ref = dataset.table('us_states_from_gcs')

# Start the load job
load_job = client.load_table_from_uri(
    uri, destination_table_ref, job_config=job_config)
print('Starting job {}'.format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print('Job finished.')

# Retrieve the destination table
destination_table = client.get_table(table_ref)
print('Loaded {} rows.'.format(destination_table.num_rows))
```

## Cleaning Up

The following code deletes the dataset created for this tutorial, including all tables in the dataset.


```python
# Retrieve the dataset from the API
dataset = client.get_dataset(client.dataset(dataset_id))

# Delete the dataset and its contents
client.delete_dataset(dataset, delete_contents=True)

print('Deleted dataset: {}'.format(dataset.path))
```
