# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Delete this file after approving /embeddings/batch_example_test.py
import os

import backoff

from google.api_core.exceptions import ResourceExhausted

import pytest

import embedding_batch


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
@pytest.fixture(scope="session", autouse=True)
def test_embed_text_batch() -> None:
    os.environ["GCS_OUTPUT_URI"] = "gs://python-docs-samples-tests/"
    batch_prediction_job = embedding_batch.embed_text_batch()
    assert batch_prediction_job
