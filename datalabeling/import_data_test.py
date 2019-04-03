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

import import_data
import manage_dataset

PROJECT_ID = os.getenv('GCLOUD_PROJECT')


@pytest.mark.slow
def test_import_data(capsys):
    # Generates a dataset_resource_name.
    manage_dataset.create_dataset(PROJECT_ID)
    out, _ = capsys.readouterr()
    create_dataset_output = out.splitlines()
    dataset_resource_name = create_dataset_output[0].split()[4]

    # Starts to test the import_data.
    import_data.import_data(
            dataset_resource_name, 'IMAGE',
            'gs://cloud-samples-data/datalabeling/image/image_dataset.csv')
    out, _ = capsys.readouterr()
    assert 'Dataset resource name: ' in out

    # Deletes the created dataset.
    manage_dataset.delete_dataset(dataset_resource_name)
