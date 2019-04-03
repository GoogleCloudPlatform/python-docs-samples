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

import manage_dataset

PROJECT_ID = os.getenv("GCLOUD_PROJECT")


@pytest.mark.slow
def test_manage_dataset(capsys):
    # Creates a dataset.
    manage_dataset.create_dataset(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out
    create_dataset_output = out.splitlines()
    created_dataset_resource_name = create_dataset_output[0].split()[4]

    # Lists the datasets
    manage_dataset.list_datasets(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out

    # Gets the dataset.
    manage_dataset.get_dataset(created_dataset_resource_name)
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out

    # Deletes the dataset.
    manage_dataset.delete_dataset(created_dataset_resource_name)
    out, _ = capsys.readouterr()
    assert "Dataset deleted." in out
