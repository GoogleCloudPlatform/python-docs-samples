#!/usr/bin/env python

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

"""This application demonstrates how to do basic operations using Cloud
Spanner.

For more information, see the README.rst under /spanner.
"""

import argparse

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types


# [START spanner_create_database]
def create_database(instance_id, database_id):
    """Creates a database and tables for sample data."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id, ddl_statements=[
        """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX)
        ) PRIMARY KEY (SingerId)""",
        """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE"""
    ])

    operation = database.create()

    print('Waiting for operation to complete...')
    operation.result()

    print('Created database {} on instance {}'.format(
        database_id, instance_id))
# [END spanner_create_database]


# [START spanner_insert_data]
def insert_data(instance_id, database_id):
    """Inserts sample data into the given database.

    The database and table must already exist and can be created using
    `create_database`.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table='Singers',
            columns=('SingerId', 'FirstName', 'LastName',),
            values=[
                (1, u'Marc', u'Richards'),
                (2, u'Catalina', u'Smith'),
                (3, u'Alice', u'Trentor'),
                (4, u'Lea', u'Martin'),
                (5, u'David', u'Lomond')])

        batch.insert(
            table='Albums',
            columns=('SingerId', 'AlbumId', 'AlbumTitle',),
            values=[
                (1, 1, u'Total Junk'),
                (1, 2, u'Go, Go, Go'),
                (2, 1, u'Green'),
                (2, 2, u'Forever Hold Your Peace'),
                (2, 3, u'Terrified')])

    print('Inserted data.')
# [END spanner_insert_data]


# [START spanner_query_data]
def query_data(instance_id, database_id):
    """Queries sample data from the database using SQL."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            'SELECT SingerId, AlbumId, AlbumTitle FROM Albums')

        for row in results:
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_query_data]


# [START spanner_read_data]
def read_data(instance_id, database_id):
    """Reads sample data from the database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        keyset = spanner.KeySet(all_=True)
        results = snapshot.read(
            table='Albums',
            columns=('SingerId', 'AlbumId', 'AlbumTitle',),
            keyset=keyset,)

        for row in results:
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_read_data]


# [START spanner_read_stale_data]
def read_stale_data(instance_id, database_id):
    """Reads sample data from the database. The data is exactly 15 seconds
    stale."""
    import datetime

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    staleness = datetime.timedelta(seconds=15)

    with database.snapshot(exact_staleness=staleness) as snapshot:
        keyset = spanner.KeySet(all_=True)
        results = snapshot.read(
            table='Albums',
            columns=('SingerId', 'AlbumId', 'AlbumTitle',),
            keyset=keyset)

        for row in results:
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_read_stale_data]


# [START spanner_query_data_with_new_column]
def query_data_with_new_column(instance_id, database_id):
    """Queries sample data from the database using SQL.

    This sample uses the `MarketingBudget` column. You can add the column
    by running the `add_column` sample or by running this DDL statement against
    your database:

        ALTER TABLE Albums ADD COLUMN MarketingBudget INT64
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            'SELECT SingerId, AlbumId, MarketingBudget FROM Albums')

        for row in results:
            print(
                u'SingerId: {}, AlbumId: {}, MarketingBudget: {}'.format(*row))
# [END spanner_query_data_with_new_column]


# [START spanner_create_index]
def add_index(instance_id, database_id):
    """Adds a simple index to the example database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    operation = database.update_ddl([
        'CREATE INDEX AlbumsByAlbumTitle ON Albums(AlbumTitle)'])

    print('Waiting for operation to complete...')
    operation.result()

    print('Added the AlbumsByAlbumTitle index.')
# [END spanner_create_index]


# [START spanner_query_data_with_index]
def query_data_with_index(
        instance_id, database_id, start_title='Aardvark', end_title='Goo'):
    """Queries sample data from the database using SQL and an index.

    The index must exist before running this sample. You can add the index
    by running the `add_index` sample or by running this DDL statement against
    your database:

        CREATE INDEX AlbumsByAlbumTitle ON Albums(AlbumTitle)

    This sample also uses the `MarketingBudget` column. You can add the column
    by running the `add_column` sample or by running this DDL statement against
    your database:

        ALTER TABLE Albums ADD COLUMN MarketingBudget INT64

    """
    from google.cloud.spanner_v1.proto import type_pb2

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    params = {
        'start_title': start_title,
        'end_title': end_title
    }
    param_types = {
        'start_title': type_pb2.Type(code=type_pb2.STRING),
        'end_title': type_pb2.Type(code=type_pb2.STRING)
    }

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT AlbumId, AlbumTitle, MarketingBudget "
            "FROM Albums@{FORCE_INDEX=AlbumsByAlbumTitle} "
            "WHERE AlbumTitle >= @start_title AND AlbumTitle < @end_title",
            params=params, param_types=param_types)

        for row in results:
            print(
                u'AlbumId: {}, AlbumTitle: {}, '
                'MarketingBudget: {}'.format(*row))
# [END spanner_query_data_with_index]


# [START spanner_read_data_with_index]
def read_data_with_index(instance_id, database_id):
    """Reads sample data from the database using an index.

    The index must exist before running this sample. You can add the index
    by running the `add_index` sample or by running this DDL statement against
    your database:

        CREATE INDEX AlbumsByAlbumTitle ON Albums(AlbumTitle)

    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        keyset = spanner.KeySet(all_=True)
        results = snapshot.read(
            table='Albums',
            columns=('AlbumId', 'AlbumTitle'),
            keyset=keyset,
            index='AlbumsByAlbumTitle')

        for row in results:
            print('AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_read_data_with_index]


# [START spanner_create_storing_index]
def add_storing_index(instance_id, database_id):
    """Adds an storing index to the example database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    operation = database.update_ddl([
        'CREATE INDEX AlbumsByAlbumTitle2 ON Albums(AlbumTitle)'
        'STORING (MarketingBudget)'])

    print('Waiting for operation to complete...')
    operation.result()

    print('Added the AlbumsByAlbumTitle2 index.')
# [END spanner_create_storing_index]


# [START spanner_read_data_with_storing_index]
def read_data_with_storing_index(instance_id, database_id):
    """Reads sample data from the database using an index with a storing
    clause.

    The index must exist before running this sample. You can add the index
    by running the `add_soring_index` sample or by running this DDL statement
    against your database:

        CREATE INDEX AlbumsByAlbumTitle2 ON Albums(AlbumTitle)
        STORING (MarketingBudget)

    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        keyset = spanner.KeySet(all_=True)
        results = snapshot.read(
            table='Albums',
            columns=('AlbumId', 'AlbumTitle', 'MarketingBudget'),
            keyset=keyset,
            index='AlbumsByAlbumTitle2')

        for row in results:
            print(
                u'AlbumId: {}, AlbumTitle: {}, '
                'MarketingBudget: {}'.format(*row))
# [END spanner_read_data_with_storing_index]


# [START spanner_add_column]
def add_column(instance_id, database_id):
    """Adds a new column to the Albums table in the example database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    operation = database.update_ddl([
        'ALTER TABLE Albums ADD COLUMN MarketingBudget INT64'])

    print('Waiting for operation to complete...')
    operation.result()

    print('Added the MarketingBudget column.')
# [END spanner_add_column]


# [START spanner_update_data]
def update_data(instance_id, database_id):
    """Updates sample data in the database.

    This updates the `MarketingBudget` column which must be created before
    running this sample. You can add the column by running the `add_column`
    sample or by running this DDL statement against your database:

        ALTER TABLE Albums ADD COLUMN MarketingBudget INT64

    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.update(
            table='Albums',
            columns=(
                'SingerId', 'AlbumId', 'MarketingBudget'),
            values=[
                (1, 1, 100000),
                (2, 2, 500000)])

    print('Updated data.')
# [END spanner_update_data]


# [START spanner_read_write_transaction]
def read_write_transaction(instance_id, database_id):
    """Performs a read-write transaction to update two sample records in the
    database.

    This will transfer 200,000 from the `MarketingBudget` field for the second
    Album to the first Album. If the `MarketingBudget` is too low, it will
    raise an exception.

    Before running this sample, you will need to run the `update_data` sample
    to populate the fields.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    def update_albums(transaction):
        # Read the second album budget.
        second_album_keyset = spanner.KeySet(keys=[(2, 2)])
        second_album_result = transaction.read(
            table='Albums', columns=('MarketingBudget',),
            keyset=second_album_keyset, limit=1)
        second_album_row = list(second_album_result)[0]
        second_album_budget = second_album_row[0]

        transfer_amount = 200000

        if second_album_budget < 300000:
            # Raising an exception will automatically roll back the
            # transaction.
            raise ValueError(
                'The second album doesn\'t have enough funds to transfer')

        # Read the first album's budget.
        first_album_keyset = spanner.KeySet(keys=[(1, 1)])
        first_album_result = transaction.read(
            table='Albums', columns=('MarketingBudget',),
            keyset=first_album_keyset, limit=1)
        first_album_row = list(first_album_result)[0]
        first_album_budget = first_album_row[0]

        # Update the budgets.
        second_album_budget -= transfer_amount
        first_album_budget += transfer_amount
        print(
            'Setting first album\'s budget to {} and the second album\'s '
            'budget to {}.'.format(
                first_album_budget, second_album_budget))

        # Update the rows.
        transaction.update(
            table='Albums',
            columns=(
                'SingerId', 'AlbumId', 'MarketingBudget'),
            values=[
                (1, 1, first_album_budget),
                (2, 2, second_album_budget)])

    database.run_in_transaction(update_albums)

    print('Transaction complete.')
# [END spanner_read_write_transaction]


# [START spanner_read_only_transaction]
def read_only_transaction(instance_id, database_id):
    """Reads data inside of a read-only transaction.

    Within the read-only transaction, or "snapshot", the application sees
    consistent view of the database at a particular timestamp.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot(multi_use=True) as snapshot:
        # Read using SQL.
        results = snapshot.execute_sql(
            'SELECT SingerId, AlbumId, AlbumTitle FROM Albums')

        print('Results from first read:')
        for row in results:
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))

        # Perform another read using the `read` method. Even if the data
        # is updated in-between the reads, the snapshot ensures that both
        # return the same data.
        keyset = spanner.KeySet(all_=True)
        results = snapshot.read(
            table='Albums',
            columns=('SingerId', 'AlbumId', 'AlbumTitle',),
            keyset=keyset,)

        print('Results from second read:')
        for row in results:
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_read_only_transaction]


# [START spanner_create_table_with_timestamp_column]
def create_table_with_timestamp(instance_id, database_id):
    """Creates a table with a COMMIT_TIMESTAMP column."""

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    operation = database.update_ddl([
        """CREATE TABLE Performances (
            SingerId     INT64 NOT NULL,
            VenueId      INT64 NOT NULL,
            EventDate    Date,
            Revenue      INT64,
            LastUpdateTime TIMESTAMP NOT NULL
            OPTIONS(allow_commit_timestamp=true)
        ) PRIMARY KEY (SingerId, VenueId, EventDate),
          INTERLEAVE IN PARENT Singers ON DELETE CASCADE"""
    ])

    print('Waiting for operation to complete...')
    operation.result()

    print('Created Performances table on database {} on instance {}'.format(
        database_id, instance_id))
# [END spanner_create_table_with_timestamp_column]


# [START spanner_insert_data_with_timestamp_column]
def insert_data_with_timestamp(instance_id, database_id):
    """Inserts data with a COMMIT_TIMESTAMP field into a table. """

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table='Performances',
            columns=(
                'SingerId', 'VenueId', 'EventDate',
                'Revenue', 'LastUpdateTime',),
            values=[
                (1, 4, "2017-10-05", 11000, spanner.COMMIT_TIMESTAMP),
                (1, 19, "2017-11-02", 15000, spanner.COMMIT_TIMESTAMP),
                (2, 42, "2017-12-23", 7000, spanner.COMMIT_TIMESTAMP)])

    print('Inserted data.')
# [END spanner_insert_data_with_timestamp_column]


# [START spanner_add_timestamp_column]
def add_timestamp_column(instance_id, database_id):
    """ Adds a new TIMESTAMP column to the Albums table in the example database.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    operation = database.update_ddl([
        'ALTER TABLE Albums ADD COLUMN LastUpdateTime TIMESTAMP '
        'OPTIONS(allow_commit_timestamp=true)'])

    print('Waiting for operation to complete...')
    operation.result()

    print('Altered table "Albums" on database {} on instance {}.'.format(
        database_id, instance_id))
# [END spanner_add_timestamp_column]


# [START spanner_update_data_with_timestamp_column]
def update_data_with_timestamp(instance_id, database_id):
    """Updates Performances tables in the database with the COMMIT_TIMESTAMP
    column.

    This updates the `MarketingBudget` column which must be created before
    running this sample. You can add the column by running the `add_column`
    sample or by running this DDL statement against your database:

        ALTER TABLE Albums ADD COLUMN MarketingBudget INT64

    In addition this update expects the LastUpdateTime column added by
    applying this DDL statement against your database:

        ALTER TABLE Albums ADD COLUMN LastUpdateTime TIMESTAMP
        OPTIONS(allow_commit_timestamp=true)
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    with database.batch() as batch:
        batch.update(
            table='Albums',
            columns=(
                'SingerId', 'AlbumId', 'MarketingBudget', 'LastUpdateTime'),
            values=[
                (1, 4, 11000, spanner.COMMIT_TIMESTAMP),
                (1, 19, 15000, spanner.COMMIT_TIMESTAMP),
                (2, 42, 7000, spanner.COMMIT_TIMESTAMP)])

    print('Updated data.')
# [END spanner_update_data_with_timestamp_column]


# [START spanner_query_data_with_timestamp_column]
def query_data_with_timestamp(instance_id, database_id):
    """Queries sample data from the database using SQL.

    This updates the `LastUpdateTime` column which must be created before
    running this sample. You can add the column by running the
    `add_timestamp_column` sample or by running this DDL statement
    against your database:

        ALTER TABLE Performances ADD COLUMN LastUpdateTime TIMESTAMP
        OPTIONS (allow_commit_timestamp=true)

    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            'SELECT SingerId, AlbumId, AlbumTitle FROM Albums '
            'ORDER BY LastUpdateTime DESC')

    for row in results:
        print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
# [END spanner_query_data_with_timestamp_column]


# [START spanner_write_data_for_struct_queries]
def write_struct_data(instance_id, database_id):
    """Inserts sample data that can be used to test STRUCT parameters
    in queries.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table='Singers',
            columns=('SingerId', 'FirstName', 'LastName',),
            values=[
                (6, u'Elena', u'Campbell'),
                (7, u'Gabriel', u'Wright'),
                (8, u'Benjamin', u'Martinez'),
                (9, u'Hannah', u'Harris')])

    print('Inserted sample data for STRUCT queries')
# [END spanner_write_data_for_struct_queries]


def query_with_struct(instance_id, database_id):
    """Query a table using STRUCT parameters. """
    # [START spanner_create_struct_with_data]
    record_type = param_types.Struct([
            param_types.StructField('FirstName', param_types.STRING),
            param_types.StructField('LastName', param_types.STRING)
    ])
    record_value = ('Elena', 'Campbell')
    # [END spanner_create_struct_with_data]

    # [START spanner_query_data_with_struct]
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId FROM Singers WHERE "
            "(FirstName, LastName) = @name",
            params={'name': record_value},
            param_types={'name': record_type})

    for row in results:
        print(u'SingerId: {}'.format(*row))
    # [END spanner_query_data_with_struct]


def query_with_array_of_struct(instance_id, database_id):
    """Query a table using an array of STRUCT parameters. """
    # [START spanner_create_user_defined_struct]
    name_type = param_types.Struct([
        param_types.StructField('FirstName', param_types.STRING),
        param_types.StructField('LastName', param_types.STRING)])
    # [END spanner_create_user_defined_struct]

    # [START spanner_create_array_of_struct_with_data]
    band_members = [("Elena", "Campbell"),
                    ("Gabriel", "Wright"),
                    ("Benjamin", "Martinez")]
    # [END spanner_create_array_of_struct_with_data]

    # [START spanner_query_data_with_array_of_struct]
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId FROM Singers WHERE "
            "STRUCT<FirstName STRING, LastName STRING>"
            "(FirstName, LastName) IN UNNEST(@names)",
            params={'names': band_members},
            param_types={'names': param_types.Array(name_type)})

    for row in results:
            print(u'SingerId: {}'.format(*row))
    # [END spanner_query_data_with_array_of_struct]


# [START spanner_field_access_on_struct_parameters]
def query_struct_field(instance_id, database_id):
    """Query a table using field access on a STRUCT parameter. """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    name_type = param_types.Struct([
        param_types.StructField('FirstName', param_types.STRING),
        param_types.StructField('LastName', param_types.STRING)
        ])

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId FROM Singers "
            "WHERE FirstName = @name.FirstName",
            params={'name': ("Elena", "Campbell")},
            param_types={'name': name_type})

    for row in results:
            print(u'SingerId: {}'.format(*row))
# [START spanner_field_access_on_struct_parameters]


# [START spanner_field_access_on_nested_struct_parameters]
def query_nested_struct_field(instance_id, database_id):
    """Query a table using nested field access on a STRUCT parameter. """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    song_info_type = param_types.Struct([
        param_types.StructField('SongName', param_types.STRING),
        param_types.StructField(
            'ArtistNames', param_types.Array(
                param_types.Struct([
                     param_types.StructField(
                         'FirstName', param_types.STRING),
                     param_types.StructField(
                         'LastName', param_types.STRING)
                ])
            )
        )
    ])

    song_info = ('Imagination', [('Elena', 'Campbell'), ('Hannah', 'Harris')])

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId, @song_info.SongName "
            "FROM Singers WHERE "
            "STRUCT<FirstName STRING, LastName STRING>"
            "(FirstName, LastName) "
            "IN UNNEST(@song_info.ArtistNames)",
            params={
                'song_info': song_info
                },
            param_types={
                'song_info': song_info_type
                }
        )

    for row in results:
            print(u'SingerId: {} SongName: {}'.format(*row))
# [END spanner_field_access_on_nested_struct_parameters]


if __name__ == '__main__':  # noqa: C901
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'instance_id', help='Your Cloud Spanner instance ID.')
    parser.add_argument(
        '--database-id', help='Your Cloud Spanner database ID.',
        default='example_db')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create_database', help=create_database.__doc__)
    subparsers.add_parser('insert_data', help=insert_data.__doc__)
    subparsers.add_parser('query_data', help=query_data.__doc__)
    subparsers.add_parser('read_data', help=read_data.__doc__)
    subparsers.add_parser('read_stale_data', help=read_stale_data.__doc__)
    subparsers.add_parser('add_column', help=add_column.__doc__)
    subparsers.add_parser('update_data', help=update_data.__doc__)
    subparsers.add_parser(
        'query_data_with_new_column', help=query_data_with_new_column.__doc__)
    subparsers.add_parser(
        'read_write_transaction', help=read_write_transaction.__doc__)
    subparsers.add_parser(
        'read_only_transaction', help=read_only_transaction.__doc__)
    subparsers.add_parser('add_index', help=add_index.__doc__)
    query_data_with_index_parser = subparsers.add_parser(
        'query_data_with_index', help=query_data_with_index.__doc__)
    query_data_with_index_parser.add_argument(
        '--start_title', default='Aardvark')
    query_data_with_index_parser.add_argument(
        '--end_title', default='Goo')
    subparsers.add_parser('read_data_with_index', help=insert_data.__doc__)
    subparsers.add_parser('add_storing_index', help=add_storing_index.__doc__)
    subparsers.add_parser(
        'read_data_with_storing_index', help=insert_data.__doc__)
    subparsers.add_parser(
        'create_table_with_timestamp',
        help=create_table_with_timestamp.__doc__)
    subparsers.add_parser(
        'insert_data_with_timestamp', help=insert_data_with_timestamp.__doc__)
    subparsers.add_parser(
        'add_timestamp_column', help=add_timestamp_column.__doc__)
    subparsers.add_parser(
        'update_data_with_timestamp', help=update_data_with_timestamp.__doc__)
    subparsers.add_parser(
        'query_data_with_timestamp', help=query_data_with_timestamp.__doc__)
    subparsers.add_parser('write_struct_data', help=write_struct_data.__doc__)
    subparsers.add_parser('query_with_struct', help=query_with_struct.__doc__)
    subparsers.add_parser(
        'query_with_array_of_struct', help=query_with_array_of_struct.__doc__)
    subparsers.add_parser(
            'query_struct_field', help=query_struct_field.__doc__)
    subparsers.add_parser(
        'query_nested_struct_field', help=query_nested_struct_field.__doc__)

    args = parser.parse_args()

    if args.command == 'create_database':
        create_database(args.instance_id, args.database_id)
    elif args.command == 'insert_data':
        insert_data(args.instance_id, args.database_id)
    elif args.command == 'query_data':
        query_data(args.instance_id, args.database_id)
    elif args.command == 'read_data':
        read_data(args.instance_id, args.database_id)
    elif args.command == 'read_stale_data':
        read_stale_data(args.instance_id, args.database_id)
    elif args.command == 'add_column':
        add_column(args.instance_id, args.database_id)
    elif args.command == 'update_data':
        update_data(args.instance_id, args.database_id)
    elif args.command == 'query_data_with_new_column':
        query_data_with_new_column(args.instance_id, args.database_id)
    elif args.command == 'read_write_transaction':
        read_write_transaction(args.instance_id, args.database_id)
    elif args.command == 'read_only_transaction':
        read_only_transaction(args.instance_id, args.database_id)
    elif args.command == 'add_index':
        add_index(args.instance_id, args.database_id)
    elif args.command == 'query_data_with_index':
        query_data_with_index(
            args.instance_id, args.database_id,
            args.start_title, args.end_title)
    elif args.command == 'read_data_with_index':
        read_data_with_index(args.instance_id, args.database_id)
    elif args.command == 'add_storing_index':
        add_storing_index(args.instance_id, args.database_id)
    elif args.command == 'read_data_with_storing_index':
        read_data_with_storing_index(args.instance_id, args.database_id)
    elif args.command == 'create_table_with_timestamp':
        create_table_with_timestamp(args.instance_id, args.database_id)
    elif args.command == 'insert_data_with_timestamp':
        insert_data_with_timestamp(args.instance_id, args.database_id)
    elif args.command == 'add_timestamp_column':
        add_timestamp_column(args.instance_id, args.database_id)
    elif args.command == 'update_data_with_timestamp':
        update_data_with_timestamp(args.instance_id, args.database_id)
    elif args.command == 'query_data_with_timestamp':
        query_data_with_timestamp(args.instance_id, args.database_id)
    elif args.command == 'write_struct_data':
        write_struct_data(args.instance_id, args.database_id)
    elif args.command == 'query_with_struct':
        query_with_struct(args.instance_id, args.database_id)
    elif args.command == 'query_with_array_of_struct':
        query_with_array_of_struct(args.instance_id, args.database_id)
    elif args.command == 'query_struct_field':
        query_struct_field(args.instance_id, args.database_id)
    elif args.command == 'query_nested_struct_field':
        query_nested_struct_field(args.instance_id, args.database_id)
