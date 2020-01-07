# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This application demonstrates how to do batch operations from a csv file
# using Cloud Spanner.
# For more information, see the README.rst.
"""Test for batch_import"""
import os
import pytest
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
    instance = spanner_client.instance(INSTANCE_ID)
    database = instance.database(DATABASE_ID)

    if not database.exists():
        with open('schema.ddl', 'r') as myfile:
            schema = myfile.read()
        database = instance.database(DATABASE_ID, ddl_statements=[schema])
        database.create()

        yield database
        database.drop()


def test_is_bool_null():
    assert batch_import.is_bool_null(['12', 'true', '', '12',
                                      'jkl', '']) == [['12'], [True],
                                                      [], ['12'],
                                                      ['jkl'], []]


def test_divide_chunks():
    res = list(batch_import.divide_chunks(['12', 'true', '', '12',
                                           'jkl', ''], 2))
    assert res == [['12', 'true'], ['', '12'], ['jkl', '']]


def test_insert_data(capsys):
    batch_import.main(INSTANCE_ID, DATABASE_ID)
    out, _ = capsys.readouterr()
    assert 'Finished Inserting Data.' in out
