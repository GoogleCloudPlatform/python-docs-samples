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

from gcp.testing.flaky import flaky

from export_data_to_cloud_storage import main

DATASET_ID = 'test_dataset'
TABLE_ID = 'test_table'


@flaky
def test_export_table_csv(cloud_config):
    cloud_storage_output_uri = \
        'gs://{}/output.csv'.format(cloud_config.storage_bucket)
    main(
        cloud_storage_output_uri,
        cloud_config.project,
        DATASET_ID,
        TABLE_ID,
        num_retries=5,
        interval=1,
        export_format="CSV")


@flaky
def test_export_table_json(cloud_config):
    cloud_storage_output_uri = \
        'gs://{}/output.json'.format(cloud_config.storage_bucket)
    main(
        cloud_storage_output_uri,
        cloud_config.project,
        DATASET_ID,
        TABLE_ID,
        num_retries=5,
        interval=1,
        export_format="NEWLINE_DELIMITED_JSON")


@flaky
def test_export_table_avro(cloud_config):
    cloud_storage_output_uri = \
        'gs://{}/output.avro'.format(cloud_config.storage_bucket)
    main(
        cloud_storage_output_uri,
        cloud_config.project,
        DATASET_ID,
        TABLE_ID,
        num_retries=5,
        interval=1,
        export_format="AVRO")
