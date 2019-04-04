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

import manage_dataset
import pytest

PROJECT_ID = os.getenv("GCLOUD_PROJECT")


@pytest.fixture(scope='function')
def dataset():
    # create a temporary dataset
    dataset = manage_dataset.create_dataset(PROJECT_ID)

    yield dataset

    # tear down
    manage_dataset.delete_dataset(dataset.name)


def test_create_dataset(capsys):
    response = manage_dataset.create_dataset(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out

    # clean up
    manage_dataset.delete_dataset(response.name)


def test_list_dataset(capsys, dataset):
    manage_dataset.list_datasets(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert dataset.name in out


def test_get_dataset(capsys, dataset):
    manage_dataset.get_dataset(dataset.name)
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out


def test_delete_dataset(capsys):
    # Creates a dataset.
    response = manage_dataset.create_dataset(PROJECT_ID)

    manage_dataset.delete_dataset(response.name)
    out, _ = capsys.readouterr()
    assert "Dataset deleted." in out
