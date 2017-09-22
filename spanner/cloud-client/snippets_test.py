# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import random
import string

from gcp_devrel.testing import eventually_consistent
from google.cloud import spanner
import pytest

import snippets

SPANNER_INSTANCE = os.environ['SPANNER_INSTANCE']


@pytest.fixture(scope='module')
def spanner_instance():
    spanner_client = spanner.Client()
    return spanner_client.instance(SPANNER_INSTANCE)


def unique_database_id():
    return 'test-db-{}'.format(''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(5)))


def test_create_database(spanner_instance):
    database_id = unique_database_id()
    print(SPANNER_INSTANCE, database_id)
    snippets.create_database(SPANNER_INSTANCE, database_id)

    database = spanner_instance.database(database_id)
    database.reload()  # Will only succeed if the database exists.
    database.drop()


@pytest.fixture(scope='module')
def temporary_database(spanner_instance):
    database_id = unique_database_id()
    snippets.create_database(SPANNER_INSTANCE, database_id)
    snippets.insert_data(SPANNER_INSTANCE, database_id)
    database = spanner_instance.database(database_id)
    database.reload()
    yield database
    database.drop()


def test_query_data(temporary_database, capsys):
    snippets.query_data(SPANNER_INSTANCE, temporary_database.database_id)

    out, _ = capsys.readouterr()

    assert 'Total Junk' in out


def test_read_data(temporary_database, capsys):
    snippets.read_data(SPANNER_INSTANCE, temporary_database.database_id)

    out, _ = capsys.readouterr()

    assert 'Total Junk' in out


def test_read_stale_data(temporary_database, capsys):
    snippets.read_stale_data(SPANNER_INSTANCE, temporary_database.database_id)

    out, _ = capsys.readouterr()

    # It shouldn't be in the output because it was *just* inserted by the
    # temporary database fixture and this sample reads 10 seconds into the
    # past.
    assert 'Total Junk' not in out


@pytest.fixture(scope='module')
def temporary_database_with_column(temporary_database):
    snippets.add_column(SPANNER_INSTANCE, temporary_database.database_id)
    yield temporary_database


def test_update_data(temporary_database_with_column):
    snippets.update_data(
        SPANNER_INSTANCE,
        temporary_database_with_column.database_id)


def test_query_data_with_new_column(temporary_database_with_column, capsys):
    snippets.query_data_with_new_column(
        SPANNER_INSTANCE,
        temporary_database_with_column.database_id)

    out, _ = capsys.readouterr()
    assert 'MarketingBudget' in out


@pytest.fixture(scope='module')
def temporary_database_with_indexes(temporary_database_with_column):
    snippets.add_index(
        SPANNER_INSTANCE,
        temporary_database_with_column.database_id)
    snippets.add_storing_index(
        SPANNER_INSTANCE,
        temporary_database_with_column.database_id)

    yield temporary_database_with_column


@pytest.mark.slow
def test_query_data_with_index(temporary_database_with_indexes, capsys):
    @eventually_consistent.call
    def _():
        snippets.query_data_with_index(
            SPANNER_INSTANCE,
            temporary_database_with_indexes.database_id)

        out, _ = capsys.readouterr()
        assert 'Go, Go, Go' in out


@pytest.mark.slow
def test_read_data_with_index(temporary_database_with_indexes, capsys):
    @eventually_consistent.call
    def _():
        snippets.read_data_with_index(
            SPANNER_INSTANCE,
            temporary_database_with_indexes.database_id)

        out, _ = capsys.readouterr()
        assert 'Go, Go, Go' in out


@pytest.mark.slow
def test_read_data_with_storing_index(temporary_database_with_indexes, capsys):
    @eventually_consistent.call
    def _():
        snippets.read_data_with_storing_index(
            SPANNER_INSTANCE,
            temporary_database_with_indexes.database_id)

        out, _ = capsys.readouterr()
        assert 'Go, Go, Go' in out


@pytest.mark.slow
def test_read_write_transaction(temporary_database_with_column, capsys):
    @eventually_consistent.call
    def _():
        snippets.update_data(
            SPANNER_INSTANCE,
            temporary_database_with_column.database_id)
        snippets.read_write_transaction(
            SPANNER_INSTANCE,
            temporary_database_with_column.database_id)

        out, _ = capsys.readouterr()

        assert '300000' in out


@pytest.mark.slow
def test_read_only_transaction(temporary_database, capsys):
    @eventually_consistent.call
    def _():
        snippets.read_only_transaction(
            SPANNER_INSTANCE,
            temporary_database.database_id)

        out, _ = capsys.readouterr()

        assert 'Forever Hold Your Peace' in out
