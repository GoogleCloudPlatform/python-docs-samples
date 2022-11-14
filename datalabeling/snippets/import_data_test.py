#!/usr/bin/env python

# Copyright 2022 Google, Inc
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

import backoff
from google.api_core.exceptions import ServerError
from google.cloud import datalabeling
import pytest

import import_data
import testing_lib

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
INPUT_GCS_URI = "gs://cloud-samples-data/datalabeling/image/image_dataset.csv"


@pytest.fixture(scope="module")
def dataset():
    # create a temporary dataset
    dataset = testing_lib.create_dataset(PROJECT_ID)

    yield dataset

    # tear down
    testing_lib.delete_dataset(dataset.name)


@pytest.mark.skip(reason="service is limited due to covid")
def test_import_data(capsys, dataset):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        import_data.import_data(
            dataset.name, datalabeling.DataType.IMAGE, INPUT_GCS_URI
        )

    run_sample()
    out, _ = capsys.readouterr()
    assert "Dataset resource name: " in out
