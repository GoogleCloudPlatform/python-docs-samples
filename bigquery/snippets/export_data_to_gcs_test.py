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

import export_data_to_gcs

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
DATASET_ID = 'test_dataset'
TABLE_ID = 'test_table'


def test_export_data_to_gcs(capsys):
    export_data_to_gcs.export_data_to_gcs(
        DATASET_ID,
        TABLE_ID,
        'gs://{}/test-export-data-to-gcs.csv'.format(BUCKET))

    out, _ = capsys.readouterr()

    assert 'Exported' in out
