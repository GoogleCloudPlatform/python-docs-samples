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

import label_text
import testing_lib

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
INPUT_GCS_URI = "gs://cloud-samples-data/datalabeling/text/input.csv"
INSTRUCTION_GCS_URI = "gs://cloud-samples-data/datalabeling" "/instruction/test.pdf"


@pytest.fixture(scope="module")
def dataset():
    # create a temporary dataset
    dataset = testing_lib.create_dataset(PROJECT_ID)

    testing_lib.import_data(dataset.name, "TEXT", INPUT_GCS_URI)

    yield dataset

    # tear down
    testing_lib.delete_dataset(dataset.name)


@pytest.fixture(scope="module")
def annotation_spec_set():
    # create a temporary annotation_spec_set
    response = testing_lib.create_annotation_spec_set(PROJECT_ID)

    yield response

    testing_lib.delete_annotation_spec_set(response.name)


@pytest.fixture(scope="module")
def instruction():
    # create a temporary instruction
    instruction = testing_lib.create_instruction(
        PROJECT_ID, datalabeling.DataType.IMAGE, INSTRUCTION_GCS_URI
    )

    yield instruction

    # tear down
    testing_lib.delete_instruction(instruction.name)


@pytest.fixture(scope="module")
def cleaner():
    resource_names = []

    yield resource_names

    for resource_name in resource_names:
        testing_lib.cancel_operation(resource_name)


# Passing in dataset as the last argument in test_label_image since it needs
# to be deleted before the annotation_spec_set can be deleted.
@pytest.mark.skip("Constantly failing")
def test_label_text(capsys, annotation_spec_set, instruction, dataset, cleaner):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        # Start labeling.
        return label_text.label_text(
            dataset.name, instruction.name, annotation_spec_set.name
        )

    response = run_sample()
    cleaner.append(response.operation.name)

    out, _ = capsys.readouterr()
    assert "Label_text operation name: " in out

    # Cancels the labeling operation.
    response.cancel()
    assert response.cancelled() is True
