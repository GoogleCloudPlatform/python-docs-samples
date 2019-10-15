# Copyright 2019 Google LLC
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
import pytest
import uuid
import batch_translate_text 
from google.cloud import storage

PROJECT_ID = os.environ['GCLOUD_PROJECT']

@pytest.fixture(scope='function')
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = str(uuid.uuid1())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)

def test_batch_translate_text(capsys, bucket):
    batch_translate_text.sample_batch_translate_text(
        'gs://cloud-samples-data/translation/text.txt',
        'gs://{}/translation/BATCH_TRANSLATION_OUTPUT/'.format(bucket.name),
        PROJECT_ID,
        'us-central1',
        'en',
        'es'
        )
    out, _ = capsys.readouterr()
    assert 'Total Characters: 13' in out
    assert 'Translated Characters: 13' in out