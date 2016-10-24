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

"""Sample that runs a file containing INSERT SQL statements in Big Query.

This could be used to run the INSERT statements in a mysqldump output such as

    mysqldump --user=root \
        --password='secret-password' \
        --host=127.0.0.1 \
        --no-create-info sample_db \
        --skip-add-locks > sample_db_export.sql

To run, first create tables with the same names and columns as the sample
database. Then run this script.

    python insert_sql.py my-project my_dataset sample_db_export.sql
"""

# [START insert_sql]
import argparse

from google.cloud import bigquery


def insert_sql(project, default_dataset, sql_path):
    """Run all the SQL statements in a SQL file."""

    client = bigquery.Client(project=project)

    with open(sql_path) as f:
        for line in f:
            line = line.strip()

            if not line.startswith('INSERT'):
                continue

            print('Running query: {}{}'.format(
                line[:60],
                '...' if len(line) > 60 else ''))
            query = client.run_sync_query(line)

            # Set use_legacy_sql to False to enable standard SQL syntax.
            # This is required to use the Data Manipulation Language features.
            #
            # For more information about enabling standard SQL, see:
            # https://cloud.google.com/bigquery/sql-reference/enabling-standard-sql
            query.use_legacy_sql = False
            query.default_dataset = client.dataset(default_dataset)
            query.run()


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('project', help='Google Cloud project name')
        parser.add_argument(
            'default_dataset', help='Default BigQuery dataset name')
        parser.add_argument('sql_path', help='Path to SQL file')

        args = parser.parse_args()

        insert_sql(args.project, args.default_dataset, args.sql_path)
# [END insert_sql]
