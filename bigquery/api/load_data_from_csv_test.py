# Copyright 2015, Google, Inc.
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

from gcp_devrel.testing.flaky import flaky

from load_data_from_csv import main

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
PROJECT = os.environ['GCLOUD_PROJECT']
BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
DATASET_ID = 'test_dataset'
TABLE_ID = 'test_import_table'


@flaky
def test_load_table():
    cloud_storage_input_uri = 'gs://{}/data.csv'.format(BUCKET)
    schema_file = os.path.join(RESOURCES, 'schema.json')

    main(
        PROJECT,
        DATASET_ID,
        TABLE_ID,
        schema_file=schema_file,
        data_path=cloud_storage_input_uri,
        poll_interval=1,
        num_retries=5
    )
