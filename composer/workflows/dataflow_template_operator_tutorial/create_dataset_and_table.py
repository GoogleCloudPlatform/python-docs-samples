# [START dataflow_composer_dataset_table_creation]

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set dataset_id to the ID of the dataset to create.
# dataset_id = "{}.average_weather".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

#TODO(developer): Fill out this location appropriately.
#dataset.location = your 

# Send the dataset to the API for creation.
# Raises google.api_core.exceptions.Conflict if the Dataset already
# exists within the project.
dataset = client.create_dataset(dataset)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))


# Next, create a table from this dataset.

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.average_weather.your_table_name"

schema = [
    bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
    bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),
    bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE")
]

table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # Make an API request.
print(
     "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)

# [END dataflow_composer_dataset_table_creation]
