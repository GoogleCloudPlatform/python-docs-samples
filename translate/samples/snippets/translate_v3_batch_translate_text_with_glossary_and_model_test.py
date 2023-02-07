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
import uuid

from google.cloud import storage
import pytest

import translate_v3_batch_translate_text_with_glossary_and_model

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GLOSSARY_ID = "DO_NOT_DELETE_TEST_GLOSSARY"
MODEL_ID = "TRL251293382528204800"


@pytest.fixture(scope="function")
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = "test-bucket-for-glossary-" + str(uuid.uuid1())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


def test_batch_translate_text_with_glossary_and_model(capsys, bucket):
    translate_v3_batch_translate_text_with_glossary_and_model.batch_translate_text_with_glossary_and_model(
        "gs://cloud-samples-data/translation/text_with_custom_model_and_glossary.txt",
        "gs://{}/translation/BATCH_TRANSLATION_GLOS_MODEL_OUTPUT/".format(bucket.name),
        PROJECT_ID,
        MODEL_ID,
        GLOSSARY_ID,
    )

    out, _ = capsys.readouterr()
    assert "Total Characters: 25" in out
