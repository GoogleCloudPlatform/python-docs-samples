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

import backoff
import pytest

from google.api_core.exceptions import DeadlineExceeded, GoogleAPICallError
from google.cloud.exceptions import NotFound

import translate_v3_create_glossary
import translate_v3_delete_glossary
import translate_v3_list_glossary


PROJECT_ID = os.environ["GCLOUD_PROJECT"]
GLOSSARY_INPUT_URI = "gs://cloud-samples-data/translation/glossary_ja.csv"


@pytest.fixture(scope="session")
def glossary():
    """Get the ID of a glossary available to session (do not mutate/delete)."""
    glossary_id = "must-start-with-letters-" + str(uuid.uuid1())
    translate_v3_create_glossary.create_glossary(
        PROJECT_ID, GLOSSARY_INPUT_URI, glossary_id
    )

    yield glossary_id

    # clean up
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


def test_list_glossary(capsys, glossary):
    translate_v3_list_glossary.list_glossaries(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert glossary in out
    assert "gs://cloud-samples-data/translation/glossary_ja.csv" in out
