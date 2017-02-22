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
                (1, 1, u'Go, Go, Go'),
                (1, 2, u'Total Junk'),
                (2, 1, u'Green'),
                (2, 2, u'Forever Hold Your Peace'),
                (2, 3, u'Terrified')])

    print('Inserted data.')


def query_data(instance_id, database_id):
    """Queries sample data from the database using SQL."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    results = database.execute_sql(
        'SELECT SingerId, AlbumId, AlbumTitle FROM Albums')

    for row in results:
        print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))


def read_data(instance_id, database_id):
    """Reads sample data from the database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    keyset = spanner.KeySet(all_=True)
    results = database.read(
        table='Albums',
        columns=('SingerId', 'AlbumId', 'AlbumTitle',),
        keyset=keyset,)

    for row in results:
        print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))


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

    results = database.execute_sql(
        'SELECT SingerId, AlbumId, MarketingBudget FROM Albums')

    for row in results:
        print(u'SingerId: {}, AlbumId: {}, MarketingBudget: {}'.format(*row))


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


def query_data_with_index(instance_id, database_id):
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
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    results = database.execute_sql(
        "SELECT AlbumId, AlbumTitle, MarketingBudget "
        "FROM Albums@{FORCE_INDEX=AlbumsByAlbumTitle} "
        "WHERE AlbumTitle >= 'Ardvark' AND AlbumTitle < 'Goo'")

    for row in results:
        print(
            u'AlbumId: {}, AlbumTitle: {}, '
            'MarketingBudget: {}'.format(*row))


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

    keyset = spanner.KeySet(all_=True)
    results = database.read(
        table='Albums',
        columns=('AlbumId', 'AlbumTitle'),
        keyset=keyset,
        index='AlbumsByAlbumTitle')

    for row in results:
        print('AlbumId: {}, AlbumTitle: {}'.format(*row))


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

    keyset = spanner.KeySet(all_=True)
    results = database.read(
        table='Albums',
        columns=('AlbumId', 'AlbumTitle', 'MarketingBudget'),
        keyset=keyset,
        index='AlbumsByAlbumTitle2')

    for row in results:
        print(
            u'AlbumId: {}, AlbumTitle: {}, '
            'MarketingBudget: {}'.format(*row))


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


def read_only_transaction(instance_id, database_id):
    """Reads data inside of a read-only transaction.

    Within the read-only transaction, or "snapshot", the application sees
    consistent view of the database at a particular timestamp.
    """
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
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


if __name__ == '__main__':
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
    subparsers.add_parser('add_column', help=add_column.__doc__)
    subparsers.add_parser('update_data', help=update_data.__doc__)
    subparsers.add_parser(
        'query_data_with_new_column', help=query_data_with_new_column.__doc__)
    subparsers.add_parser(
        'read_write_transaction', help=read_write_transaction.__doc__)
    subparsers.add_parser(
        'read_only_transaction', help=read_only_transaction.__doc__)
    subparsers.add_parser('add_index', help=add_index.__doc__)
    subparsers.add_parser('query_data_with_index', help=insert_data.__doc__)
    subparsers.add_parser('read_data_with_index', help=insert_data.__doc__)
    subparsers.add_parser('add_storing_index', help=add_storing_index.__doc__)
    subparsers.add_parser(
        'read_data_with_storing_index', help=insert_data.__doc__)

    args = parser.parse_args()

    if args.command == 'create_database':
        create_database(args.instance_id, args.database_id)
    elif args.command == 'insert_data':
        insert_data(args.instance_id, args.database_id)
    elif args.command == 'query_data':
        query_data(args.instance_id, args.database_id)
    elif args.command == 'read_data':
        read_data(args.instance_id, args.database_id)
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
        query_data_with_index(args.instance_id, args.database_id)
    elif args.command == 'read_data_with_index':
        read_data_with_index(args.instance_id, args.database_id)
    elif args.command == 'add_storing_index':
        add_storing_index(args.instance_id, args.database_id)
    elif args.command == 'read_data_with_storing_index':
        read_data_with_storing_index(args.instance_id, args.database_id)
