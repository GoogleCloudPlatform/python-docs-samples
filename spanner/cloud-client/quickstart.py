#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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


def run_quickstart():
    # [START spanner_quickstart]
    # Imports the Google Cloud Client Library.
    from google.cloud import spanner

    # Instantiate a client.
    spanner_client = spanner.Client()

    # Your Cloud Spanner instance ID.
    instance_id = 'my-instance-id'

    # Get a Cloud Spanner instance by ID.
    instance = spanner_client.instance(instance_id)

    # Your Cloud Spanner database ID.
    database_id = 'my-database-id'

    # Get a Cloud Spanner database by ID.
    database = instance.database(database_id)

    # Execute a simple SQL statement.
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql('SELECT 1')

        for row in results:
            print(row)
    # [END spanner_quickstart]


if __name__ == '__main__':
    run_quickstart()
