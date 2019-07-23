"""Test for batch_import"""
import unittest.mock
import os
import pytest
import batch_import
from google.cloud import spanner

def unique_database_id():
            """ Creates a unique id for the database. """
            return 'test-db-{}'.format(''.join(random.choice(
                string.ascii_lowercase + string.digits) for _ in range(5)))


INSTANCE_ID = os.environ['SPANNER_INSTANCE']
DATABASE_ID = unique_database_id()


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
                        database = instance.database(DATABASE_ID, ddl_statements=[
                        """
                        CREATE TABLE comments (
                         id INT64,
                         author STRING(MAX),
                         `by` STRING(MAX),
                         dead BOOL,
                         deleted BOOL,
                         parent INT64,
                         ranking INT64,
                         text STRING(MAX),
                         time INT64,
                         time_ts TIMESTAMP,
                        ) PRIMARY KEY(parent, id);

                        CREATE INDEX CommentsByAuthor ON comments(author);

                        CREATE TABLE stories (
                         id INT64,
                         author STRING(MAX),
                         `by` STRING(MAX),
                         dead BOOL,
                         deleted BOOL,
                         descendants INT64,
                         score INT64,
                         text STRING(MAX),
                         time INT64,
                         time_ts TIMESTAMP,
                         title STRING(MAX),
                         url STRING(MAX),
                        ) PRIMARY KEY(id);

                        CREATE INDEX StoriesByAuthor ON stories(author);

                        CRETE INDEX StoriesByScoreURL ON stories(score, url);

                        CREATE INDEX StoriesByTitleTimeScore ON stories(title) STORING (time_ts, score)

                        """
                        ])
                        database.create()

            yield database
                    database.drop()

def test_insert_data(capsys):
          batch_import.main(INSTANCE_ID,DATABASE_ID)
          out, _ = capsys.readouterr()
          assert 'Finished Inserting Data.' in out

