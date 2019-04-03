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
import pytest

import create_annotation_spec_set
import create_instruction
import import_data
import label_text
import manage_dataset

PROJECT_ID = os.getenv('GCLOUD_PROJECT')


@pytest.mark.slow
def test_label_text_pipeline(capsys):
    # Creates a dataset.
    manage_dataset.create_dataset(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'The dataset resource name:' in out
    dataset_resource_name = out.splitlines()[0].split()[4]

    # Creates an annotation_spec_set.
    create_annotation_spec_set.create_annotation_spec_set(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert 'The annotation_spec_set resource name:' in out
    annotation_spec_set_resource_name = out.splitlines()[0].split()[4]

    # Creates an instruction.
    create_instruction.create_instruction(
            PROJECT_ID, 'TEXT',
            'gs://cloud-samples-data/datalabeling/instruction/test.pdf')
    out, _ = capsys.readouterr()
    assert 'The instruction resource name:' in out
    instruction_resource_name = out.splitlines()[0].split()[4]

    # Imports data.
    import_data.import_data(
            dataset_resource_name, 'TEXT',
            'gs://cloud-samples-data/datalabeling/text/text_dataset.csv')
    out, _ = capsys.readouterr()
    assert 'Dataset resource name:' in out

    # Starts text data labeling.
    response = label_text.label_text(dataset_resource_name,
                                                                     instruction_resource_name,
                                                                     annotation_spec_set_resource_name)
    out, _ = capsys.readouterr()
    assert 'Label_text operation name: ' in out
    operation_name = response.operation.name

    # Cancels the labeling operation.
    response.cancel()
    assert response.cancelled() == True

    from google.cloud import datalabeling_v1beta1 as datalabeling
    client = datalabeling.DataLabelingServiceClient()
    cancel_response = client.transport._operations_client.cancel_operation(
            operation_name)

    # Deletes the created dataset.
    manage_dataset.delete_dataset(dataset_resource_name)
    out, _ = capsys.readouterr()
    assert 'Dataset deleted.' in out

    # Deletes the created annotation spec set.
    client.delete_annotation_spec_set(annotation_spec_set_resource_name)

    # Deletes the created instruction.
    client.delete_instruction(instruction_resource_name)
