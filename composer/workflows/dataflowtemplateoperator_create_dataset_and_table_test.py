from google.cloud import bigquery
import google.cloud.exceptions
import pytest
from . import dataflowtemplateoperator_create_dataset_and_table_helper as helper

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
def dataset():
    try:
        dataset = client.get_dataset(expected_dataset_id)
    except google.cloud.exceptions.NotFound:
        dataset = helper.create_dataset()

    yield dataset

    client.delete_dataset(dataset, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="module")
def table():
    try:
        table = client.get_table(expected_table_id)
    except google.cloud.exceptions.NotFound:
        table = helper.create_table()

    yield table

    client.delete_table(table, not_found_ok=True)


def test_creation(dataset, table):
    assert table.table_id == "average_weather"
    assert dataset.dataset_id == "average_weather"
    assert table.schema == expected_schema
