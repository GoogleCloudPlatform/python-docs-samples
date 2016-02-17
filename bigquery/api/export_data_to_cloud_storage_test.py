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
#

"""Tests for export_table_to_gcs."""
from nose.plugins.attrib import attr
from testing import CloudTest

from .export_data_to_cloud_storage import main


@attr('slow')
class TestExportTableToGCS(CloudTest):
    dataset_id = 'test_dataset'
    table_id = 'test_table'

    def test_export_table_csv(self):
        cloud_storage_output_uri = \
            'gs://{}/output.csv'.format(self.config.CLOUD_STORAGE_BUCKET)
        main(
            cloud_storage_output_uri,
            self.config.GCLOUD_PROJECT,
            self.dataset_id,
            self.table_id,
            num_retries=5,
            interval=1,
            export_format="CSV")

    def test_export_table_json(self):
        cloud_storage_output_uri = \
            'gs://{}/output.json'.format(self.config.CLOUD_STORAGE_BUCKET)
        main(
            cloud_storage_output_uri,
            self.config.GCLOUD_PROJECT,
            self.dataset_id,
            self.table_id,
            num_retries=5,
            interval=1,
            export_format="NEWLINE_DELIMITED_JSON")

    def test_export_table_avro(self):
        cloud_storage_output_uri = \
            'gs://{}/output.avro'.format(self.config.CLOUD_STORAGE_BUCKET)
        main(
            cloud_storage_output_uri,
            self.config.GCLOUD_PROJECT,
            self.dataset_id,
            self.table_id,
            num_retries=5,
            interval=1,
            export_format="AVRO")
