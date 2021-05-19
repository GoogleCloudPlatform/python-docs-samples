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

from google.cloud import storage
import pytest

import translate_v3_batch_translate_text_with_glossary


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GLOSSARY_ID = "DO_NOT_DELETE_TEST_GLOSSARY"


@pytest.fixture(scope="function")
def bucket():
    """Create a temporary bucket to store annotation output."""
    bucket_name = f"tmp-{uuid.uuid4().hex}"
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)

    yield bucket

    bucket.delete(force=True)


@pytest.mark.flaky(max_runs=3, min_passes=1)
def test_batch_translate_text_with_glossary(capsys, bucket):
    translate_v3_batch_translate_text_with_glossary.batch_translate_text_with_glossary(
        "gs://cloud-samples-data/translation/text_with_glossary.txt",
        "gs://{}/translation/BATCH_TRANSLATION_GLOS_OUTPUT/".format(bucket.name),
        PROJECT_ID,
        GLOSSARY_ID,
        320,
    )

    out, _ = capsys.readouterr()
    assert "Total Characters: 9" in out
