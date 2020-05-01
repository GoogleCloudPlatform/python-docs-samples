# Copyright 2020 Google LLC
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

import os
import uuid

import backoff
import pytest

from google.api_core.exceptions import DeadlineExceeded, GoogleAPICallError
from google.cloud.exceptions import NotFound
from google.cloud import storage

import translate_v3_batch_translate_text_with_glossary
import translate_v3_create_glossary
import translate_v3_delete_glossary


PROJECT_ID = os.environ["GCLOUD_PROJECT"]
GLOSSARY_INPUT_URI = "gs://cloud-samples-data/translation/glossary_ja.csv"


@pytest.fixture(scope="session")
def glossary():
    """Get the ID of a glossary available to session (do not mutate/delete)."""
    glossary_id = "test-{}".format(uuid.uuid4())
    translate_v3_create_glossary.create_glossary(
        PROJECT_ID, GLOSSARY_INPUT_URI, glossary_id
    )

    yield glossary_id

    # cleanup
    @backoff.on_exception(
        backoff.expo, (DeadlineExceeded, GoogleAPICallError), max_time=60
    )
    def delete_glossary():
        try:
            translate_v3_delete_glossary.delete_glossary(
                PROJECT_ID, glossary_id)
        except NotFound as e:
            # Ignoring this case.
            print("Got NotFound, detail: {}".format(str(e)))
    delete_glossary()


@pytest.fixture(scope="function")
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = str(uuid.uuid1())
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_batch_translate_text_with_glossary(capsys, bucket, glossary):
    translate_v3_batch_translate_text_with_glossary.batch_translate_text_with_glossary(
        "gs://cloud-samples-data/translation/text_with_glossary.txt",
        "gs://{}/translation/BATCH_TRANSLATION_OUTPUT/".format(bucket.name),
        PROJECT_ID,
        glossary,
    )

    out, _ = capsys.readouterr()
    assert "Total Characters: 9" in out
