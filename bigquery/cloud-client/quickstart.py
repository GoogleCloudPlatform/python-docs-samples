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
    # [START bigquery_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import bigquery

    # Instantiates a client
    bigquery_client = bigquery.Client()

    # The name for the new dataset
    dataset_name = 'my_new_dataset'

    # Prepares the new dataset
    dataset = bigquery_client.dataset(dataset_name)

    # Creates the new dataset
    dataset.create()

    print('Dataset {} created.'.format(dataset.name))
    # [END bigquery_quickstart]


if __name__ == '__main__':
    run_quickstart()
