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
from google.api_core.client_options import ClientOptions
import import_data
import label_text
import manage_dataset
import pytest
import time

PROJECT_ID = os.getenv('GCLOUD_PROJECT')
INPUT_GCS_URI = 'gs://cloud-samples-data/datalabeling/text/text_dataset.csv'


@pytest.mark.slow
def test_label_text(capsys):
    # create a temporary dataset
    dataset = manage_dataset.create_dataset(PROJECT_ID)

    # create a temporary instruction
    instruction = create_instruction.create_instruction(
            PROJECT_ID, 'TEXT',
            'gs://cloud-samples-data/datalabeling/instruction/test.pdf')

    annotation_spec = create_annotation_spec_set.create_annotation_spec_set(
        PROJECT_ID)

    # import some data to it
    import_data.import_data(dataset.name, 'TEXT', INPUT_GCS_URI)

    # Start labeling.
    response = label_text.label_text(
        dataset.name,
        instruction.name,
        annotation_spec.name
    )
    out, _ = capsys.readouterr()
    assert 'Label_text operation name: ' in out
    operation_name = response.operation.name

    # Cancels the labeling operation.
    response.cancel()
    assert response.cancelled() is True

    client = datalabeling.DataLabelingServiceClient()

    # If provided, use a provided test endpoint - this will prevent tests on
    # this snippet from triggering any action by a real human
    if 'DATALABELING_ENDPOINT' in os.environ:
        opts = ClientOptions(api_endpoint=os.getenv('DATALABELING_ENDPOINT'))
        client = datalabeling.DataLabelingServiceClient(client_options=opts)

    client.transport._operations_client.cancel_operation(
            operation_name)

    # tear down
    manage_dataset.delete_dataset(dataset.name)
    time.sleep(30)

    client.delete_annotation_spec_set(annotation_spec.name)
    client.delete_instruction(instruction.name)
