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

import backoff
from google.api_core.exceptions import DeadlineExceeded, GoogleAPICallError
from google.cloud import storage
from google.cloud.exceptions import NotFound
import pytest

import translate_v3_batch_translate_text_with_glossary_and_model
import translate_v3_create_glossary
import translate_v3_delete_glossary

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GLOSSARY_INPUT_URI = "gs://cloud-samples-data/translation/glossary_ja.csv"
MODEL_ID = "TRL3128559826197068699"


@pytest.fixture(scope="session")
def glossary():
    """Get the ID of a glossary available to session (do not mutate/delete)."""
    glossary_id = "must-start-with-letters-" + str(uuid.uuid1())
    translate_v3_create_glossary.create_glossary(
        project_id=PROJECT_ID, input_uri=GLOSSARY_INPUT_URI, glossary_id=glossary_id
    )

    yield glossary_id

    # clean up
    @backoff.on_exception(
        backoff.expo, (DeadlineExceeded, GoogleAPICallError), max_time=60
    )
    def delete_glossary():
        try:
            translate_v3_delete_glossary.delete_glossary(PROJECT_ID, glossary_id)
        except NotFound as e:
            # Ignoring this case.
            print("Got NotFound, detail: {}".format(str(e)))

    delete_glossary()


@pytest.fixture(scope="function")
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = "test-bucket-for-glossary-" + str(uuid.uuid1())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


def test_batch_translate_text_with_glossary_and_model(capsys, bucket, glossary):
    translate_v3_batch_translate_text_with_glossary_and_model.batch_translate_text_with_glossary_and_model(
        "gs://cloud-samples-data/translation/text_with_custom_model_and_glossary.txt",
        "gs://{}/translation/BATCH_TRANSLATION_GLOS_MODEL_OUTPUT/".format(bucket.name),
        PROJECT_ID,
        MODEL_ID,
        glossary,
    )

    out, _ = capsys.readouterr()
    assert "Total Characters: 25" in out
