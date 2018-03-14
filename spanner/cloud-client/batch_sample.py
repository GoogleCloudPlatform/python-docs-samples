# Copyright 2018 Google Inc. All Rights Reserved.
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

"""This application demonstrates how to do batch operations using Cloud
Spanner.

For more information, see the README.rst under /spanner.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import time

from google.cloud import spanner


# [START spanner_batch_client]
def run_batch_query(instance_id, database_id):
    """Runs an example batch query."""

    # CREATE TABLE Singers (
    #   SingerId   INT64 NOT NULL,
    #   FirstName  STRING(1024),
    #   LastName   STRING(1024),
    #   SingerInfo BYTES(MAX),
    # ) PRIMARY KEY (SingerId);

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    # Create the batch transaction and generate partitions
    batch_transaction = database.batch_transaction()
    partitions = batch_transaction.generate_read_batches(
        table='Singers',
        columns=('SingerId', 'FirstName', 'LastName',),
        keyset=spanner.KeySet(all_=True)
    )

    # Create a pool of workers for the tasks
    pool = ThreadPoolExecutor()
    results = []
    start = time.time()

    for partition in partitions:
        print('Starting partition.')
        results.append(
            pool.apply_async(
                process_partition, (batch_transaction, partition)))

    # Print results
    for result in results:
        print(result)
        finish, row_ct = result.get(timeout=3600)
        elapsed = finish - start
        print(u'Completed {} rows in {} seconds'.format(row_ct, elapsed))

    # Clean up
    batch_transaction.session.delete()


def process_partition(transaction, partition):
    """Processes the requests of a query in an separate process."""
    print('Process started.')
    try:
        row_ct = 0
        for row in transaction.process_read_batch(partition):
            print(u'SingerId: {}, AlbumId: {}, AlbumTitle: {}'.format(*row))
            row_ct += 1
        return time.time(), row_ct
    except Exception as e:
        print(e.message)
# [END spanner_batch_client]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'instance_id', help='Your Cloud Spanner instance ID.')
    parser.add_argument(
        'database_id', help='Your Cloud Spanner database ID.',
        default='example_db')

    args = parser.parse_args()

    run_batch_query(args.instance_id, args.database_id)
