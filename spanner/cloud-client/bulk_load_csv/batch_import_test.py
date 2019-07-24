"""Test for batch_import"""
import os
import pytest
import string
import random
import batch_import
from google.cloud import spanner


INSTANCE_ID = os.environ['SPANNER_INSTANCE']
DATABASE_ID = 'hnewsdb'


@pytest.fixture(scope='module')
def spanner_instance():
    spanner_client = spanner.Client()
    return spanner_client.instance(INSTANCE_ID)


@pytest.fixture
def example_database():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(SPANNER_INSTANCE)
    database = instance.database(DATABASE_ID)

    if not database.exists():
        with open('schema.ddl', 'r') as myfile:
            schema = myfile.read()
        database = instance.database(DATABASE_ID, ddl_statements=[schema])
        database.create()

        yield database
        database.drop()


def test_insert_data(capsys):
    batch_import.main(INSTANCE_ID, DATABASE_ID)
    out, _ = capsys.readouterr()
    assert 'Finished Inserting Data.' in out
