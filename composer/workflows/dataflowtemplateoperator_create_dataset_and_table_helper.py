# This script is a helper function to the Dataflow Template Operator Tutorial.
# It helps the user set up a BigQuery dataset and table that is needed
# for the tutorial.

# [START composer_dataflow_dataset_table_creation]

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set client.project to your GCP Project ID.
# client.project = "your-client-project"

dataset_id = F"{client.project}.average_weather"

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# TODO(developer): Fill out this location appropriately.
# dataset.location = your-data-location

# Send the dataset to the API for creation.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset)  # Make an API request.
print(f"Created dataset {client.project} {dataset.dataset_id}")


# Create a table from this dataset.

table_id = f"{client.project}.average_weather.average_weather"

schema = [
    bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
    bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE"),
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

# [END composer_dataflow_dataset_table_creation]
