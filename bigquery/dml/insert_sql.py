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

"""Sample to run line-separated SQL statements in Big Query from a file.

This could be used to run INSERT DML statements from a mysqldump output such as

    mysqldump --user=root \
        --password='secret-password' \
        --host=127.0.0.1 \
        --no-create-info sample_db \
        --skip-add-locks > sample_db_export.sql

To run, first create tables with the same names and columns as the sample
database. Then run this script.

    python insert_sql.py \
            --project=my-project \
            --default_dataset=my_db \
            sample_db_export.sql
"""

from __future__ import print_function

import argparse
import time

from gcloud import bigquery
from gcloud import exceptions


def retry_query(query, times=3):

    for attempt in range(times):

        try:
            query.run()
            return
        except exceptions.GCloudError as err:

            if attempt == times - 1:
                print('Giving up')
                raise

            print('Retrying, got error: {}'.format(err))
            time.sleep(1)


def insert_sql(sql_path, project=None, default_dataset=None):
    client = bigquery.Client(project=project)

    with open(sql_path) as f:
        for line in f:
            line = line.strip()

            # Ignore blank lines and comments.
            if line == '' or line.startswith('--') or line.startswith('/*'):
                continue

            print('Running query: {}{}'.format(
                line[:60],
                '...' if len(line) > 60 else ''))
            query = client.run_sync_query(line)
            query.use_legacy_sql = False

            if default_dataset is not None:
                query.default_dataset = client.dataset(default_dataset)

            retry_query(query)


if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('--project', help='Google Cloud project name')
        parser.add_argument(
                '--default-dataset', help='Default BigQuery dataset name')
        parser.add_argument('sql_path', help='Path to SQL file')

        args = parser.parse_args()

        insert_sql(args.sql_path, args.project, args.default_dataset)
