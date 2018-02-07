# Copyright 2017 Google, Inc.
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

import os

from google.cloud import storage

import pytest

import gcs_example_mqtt_device as device

gcs_bucket = os.environ['CLOUD_STORAGE_BUCKET']
cloud_region = 'us-central1'
destination_file_name = 'destination-file.bin'
project_id = os.environ['GCLOUD_PROJECT']


@pytest.fixture(scope='module')
def test_blob():
    """Provides a pre-existing blob in the test bucket."""
    bucket = storage.Client().bucket(gcs_bucket)
    # Name of the blob
    blob = bucket.blob('iot_core_store_file_gcs')
    # Text in the blob
    blob.upload_from_string('This file on GCS will go to a device.')

    yield blob
    # Clean up
    blob.delete()


def test_download_blob(test_blob, capsys):
    device.download_blob(gcs_bucket, test_blob.name, destination_file_name)

    out, _ = capsys.readouterr()
    assert 'Config {} downloaded to {}.'.format(
        test_blob.name, destination_file_name) in out
