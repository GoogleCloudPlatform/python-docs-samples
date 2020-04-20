from . import dataflowtemplateoperator_create_dataset_and_table_helper as helper
from google.cloud import bigquery
import google.cloud.exceptions
import google.api_core.exceptions
import pytest

client = bigquery.Client()

expected_schema = schema = [
    bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
    bigquery.SchemaField("average_temperature", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("month", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("inches_of_rain", "NUMERIC", mode="NULLABLE"),        
    bigquery.SchemaField("is_current", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("latest_measurement", "DATE", mode="NULLABLE"),
]

expected_table_id = f"{client.project}.average_weather.average_weather"
expected_dataset_id = f"{client.project}.average_weather"

@pytest.fixture(scope="module")
def dataset_id():
    try:
        dataset = client.get_dataset(expected_dataset_id)
        dataset_id = dataset.dataset_id
    except google.cloud.exceptions.NotFound:
        dataset_id = helper.create_dataset()

    yield dataset_id

    client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)

@pytest.fixture(scope="module")
def table():
    try:
        table = client.get_table(expected_table_id)
    except google.api_core.exceptions.NotFound:
        table = helper.create_table()

    yield table

    client.delete_table(table, not_found_ok=True)

def test_creation(dataset_id, table):

    assert table.table_id == "average_weather"
    assert dataset_id == expected_dataset_id
    assert table.schema == expected_schema
    
