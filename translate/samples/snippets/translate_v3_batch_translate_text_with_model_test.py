# Copyright 2020 Google LLC
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
import uuid

from google.cloud import storage
import pytest

import translate_v3_batch_translate_text_with_model


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
MODEL_ID = "TRL251293382528204800"


@pytest.fixture(scope="function")
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = f"tmp-{uuid.uuid4().hex}"
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


def test_batch_translate_text_with_model(capsys, bucket):
    translate_v3_batch_translate_text_with_model.batch_translate_text_with_model(
        "gs://cloud-samples-data/translation/custom_model_text.txt",
        f"gs://{bucket.name}/translation/BATCH_TRANSLATION_MODEL_OUTPUT/",
        PROJECT_ID,
        MODEL_ID,
    )
    out, _ = capsys.readouterr()
    assert "Total Characters: 15" in out
    assert "Translated Characters: 15" in out
