#!/usr/bin/env python

# Copyright 2019 Google, Inc
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

import create_annotation_spec_set
import create_instruction
from google.cloud import datalabeling_v1beta1 as datalabeling
import import_data
import label_image
import manage_dataset
import pytest

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
INPUT_GCS_URI = 'gs://cloud-samples-data/datalabeling/image/image_dataset.csv'


@pytest.fixture(scope='function')
def dataset():
    # create a temporary dataset
    dataset = manage_dataset.create_dataset(PROJECT_ID)

    # import some data to it
    import_data.import_data(dataset.name, 'IMAGE', INPUT_GCS_URI)

    yield dataset

    # tear down
    manage_dataset.delete_dataset(dataset.name)


@pytest.fixture(scope='function')
def annotation_spec_set():
    # create a temporary annotation_spec_set
    response = create_annotation_spec_set.create_annotation_spec_set(
        PROJECT_ID)

    yield response

    # tear down
    client = datalabeling.DataLabelingServiceClient()
    client.delete_annotation_spec_set(response.name)


@pytest.fixture(scope='function')
def instruction():
    # create a temporary instruction
    instruction = create_instruction.create_instruction(
            PROJECT_ID, 'IMAGE',
            'gs://cloud-samples-data/datalabeling/instruction/test.pdf')

    yield instruction

    # tear down
    client = datalabeling.DataLabelingServiceClient()
    client.delete_instruction(instruction.name)


# Passing in dataset as the last argument in test_label_image since it needs
# to be deleted before the annotation_spec_set can be deleted.
@pytest.mark.slow
def test_label_image(capsys, annotation_spec_set, instruction, dataset):

    # Start labeling.
    response = label_image.label_image(
        dataset.name,
        instruction.name,
        annotation_spec_set.name
    )
    out, _ = capsys.readouterr()
    assert 'Label_image operation name: ' in out
    operation_name = response.operation.name

    # Cancels the labeling operation.
    response.cancel()
    assert response.cancelled() is True

    client = datalabeling.DataLabelingServiceClient()
    client.transport._operations_client.cancel_operation(
            operation_name)
