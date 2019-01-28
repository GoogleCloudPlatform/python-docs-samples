
# BigQuery Basics

[BigQuery](https://cloud.google.com/bigquery/docs/) is a petabyte-scale analytics data warehouse that you can use to run SQL queries over vast amounts of data in near realtime. This page shows you how to get started with the Google BigQuery API using the Python client library.

## Import the libraries used in this tutorial


```python
from google.cloud import bigquery
import pandas
```

## Initialize a client

To use the BigQuery Python client library, start by initializing a client. The BigQuery client is used to send and receive messages from the BigQuery API.

### Client project
The project used by the client will default to the project associated with the credentials file stored in the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

See the [google-auth](https://google-auth.readthedocs.io/en/latest/reference/google.auth.html) for more information about Application Default Credentials.


### Client location
Locations are required for certain BigQuery operations such as creating a Dataset. If a location is provided to the client when it is initialized, it will be the default location for jobs, datasets, and tables.

Run the following to create a client with your default project:


```python
client = bigquery.Client(location="US")
print("Client creating using default project: {}".format(client.project))
```

    Client creating using default project: your-project-id


Alternatively, you can explicitly specify a project when constructing the client:


```python
client = bigquery.Client(location="US", project="your-project-id")
```

## Run a query on a public dataset

The following example runs a query on the BigQuery `usa_names` public dataset, which is a Social Security Administration dataset that contains all names from Social Security card applications for births that occurred in the United States after 1879.

Use the [Client.query()](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.client.Client.html#google.cloud.bigquery.client.Client.query) method to run the query, and the [QueryJob.to_dataframe()](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.QueryJob.html#google.cloud.bigquery.job.QueryJob.to_dataframe) method to return the results as a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).


```python
query = """
    SELECT name FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = "TX"
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




<div>

<table>
<thead>
<tr>
<th></th>
<th>name</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>Mary</td>
</tr>
<tr>
<th>1</th>
<td>Ruby</td>
</tr>
<tr>
<th>2</th>
<td>Annie</td>
</tr>
<tr>
<th>3</th>
<td>Willie</td>
</tr>
<tr>
<th>4</th>
<td>Ruth</td>
</tr>
<tr>
<th>5</th>
<td>Gladys</td>
</tr>
<tr>
<th>6</th>
<td>Maria</td>
</tr>
<tr>
<th>7</th>
<td>Frances</td>
</tr>
<tr>
<th>8</th>
<td>Margaret</td>
</tr>
<tr>
<th>9</th>
<td>Helen</td>
</tr>
</tbody>
</table>
</div>



## Run a parameterized query

BigQuery supports query parameters to help prevent [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) when queries are constructed using user input. This feature is only available with [standard SQL syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/). Query parameters can be used as substitutes for arbitrary expressions. Parameters cannot be used as substitutes for identifiers, column names, table names, or other parts of the query.

To specify a named parameter, use the `@` character followed by an [identifier](https://cloud.google.com/bigquery/docs/reference/standard-sql/lexical#identifiers), such as `@param_name`. For example, this query finds all the words in a specific Shakespeare corpus with counts that are at least the specified value.

For more information, see [Running Parameterized Queries](https://cloud.google.com/bigquery/docs/parameterized-queries) in the BigQuery documentation.


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




<div>

<table>
<thead>
<tr>
<th></th>
<th>word</th>
<th>word_count</th>
</tr>
</thead>
<tbody>
<tr>
<th>0</th>
<td>the</td>
<td>614</td>
</tr>
<tr>
<th>1</th>
<td>I</td>
<td>577</td>
</tr>
<tr>
<th>2</th>
<td>and</td>
<td>490</td>
</tr>
<tr>
<th>3</th>
<td>to</td>
<td>486</td>
</tr>
<tr>
<th>4</th>
<td>a</td>
<td>407</td>
</tr>
<tr>
<th>5</th>
<td>of</td>
<td>367</td>
</tr>
<tr>
<th>6</th>
<td>my</td>
<td>314</td>
</tr>
<tr>
<th>7</th>
<td>is</td>
<td>307</td>
</tr>
<tr>
<th>8</th>
<td>in</td>
<td>291</td>
</tr>
<tr>
<th>9</th>
<td>you</td>
<td>271</td>
</tr>
<tr>
<th>10</th>
<td>that</td>
<td>270</td>
</tr>
<tr>
<th>11</th>
<td>me</td>
<td>263</td>
</tr>
</tbody>
</table>
</div>



## Create a new dataset

A dataset is contained within a specific [project](https://cloud.google.com/bigquery/docs/projects). Datasets are top-level containers that are used to organize and control access to your [tables](https://cloud.google.com/bigquery/docs/tables) and [views](https://cloud.google.com/bigquery/docs/views). A table or view must belong to a dataset, so you need to create at least one dataset before [loading data into BigQuery](https://cloud.google.com/bigquery/loading-data-into-bigquery).


```python
# Define a name for the new dataset.
dataset_id = 'your_new_dataset'

# The project defaults to the Client's project if not specified.
dataset = client.create_dataset(dataset_id)  # API request
```

## Write query results to a destination table

For more information, see [Writing Query Results](https://cloud.google.com/bigquery/docs/writing-results) in the BigQuery documentation.


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

    Query results loaded to table /projects/your-project-id/datasets/your_new_dataset/tables/your_new_table_id


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

    Loaded dataframe to /projects/your-project-id/datasets/your_new_dataset/tables/monty_python


## Load data from a local file to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Loading Data into BigQuery from a Local Data Source](https://cloud.google.com/bigquery/docs/loading-data-local) in the BigQuery documentation.


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

    Loaded 50 rows into your_new_dataset:/projects/your-project-id/datasets/your_new_dataset/tables/us_states_from_local_file.


## Load data from Google Cloud Storage to a table

The example below demonstrates how to load a local CSV file into a new or existing table. See [SourceFormat](https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.SourceFormat.html#google.cloud.bigquery.job.SourceFormat) in the Python client library documentation for a list of available source formats. For more information, see [Introduction to Loading Data from Cloud Storage](https://cloud.google.com/bigquery/docs/loading-data-cloud-storage) in the BigQuery documentation.


```python
# Configure the load job
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('post_abbr', 'STRING')
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
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

# Retreive the destination table
destination_table = client.get_table(table_ref)
print('Loaded {} rows.'.format(destination_table.num_rows))
```

    Starting job a27afe96-d36b-458e-b72f-ba47f3d192dc
    Job finished.
    Loaded 50 rows.


## Cleaning Up

The following code deletes the dataset created for this tutorial, including all tables in the dataset.


```python
# Retrieve the dataset from the API
dataset = client.get_dataset(client.dataset(dataset_id))

# Delete the dataset and its contents
client.delete_dataset(dataset, delete_contents=True)

print('Deleted dataset: {}'.format(dataset.path))
```

    Deleted dataset: /projects/your-project-id/datasets/your_new_dataset

