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
from google.api_core.exceptions import RetryError, ServerError
import pytest

import manage_dataset
import testing_lib

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


@pytest.mark.skip(reason="service is limited due to covid")
@pytest.fixture(scope="module")
def dataset():
    # create a temporary dataset
    dataset = testing_lib.create_dataset(PROJECT_ID)

    yield dataset

    # tear down
    testing_lib.delete_dataset(dataset.name)


@pytest.fixture(scope="module")
def cleaner():
    # First delete old datasets.
    try:
        testing_lib.delete_old_datasets(PROJECT_ID)
    # We see occational RetryError while deleting old datasets.
    # We can just ignore it and move on.
    except RetryError as e:
        print("delete_old_datasets failed: detail {}".format(e))

    resource_names = []

    yield resource_names

    for resource_name in resource_names:
        testing_lib.delete_dataset(resource_name)


@pytest.mark.skip(reason="service is limited due to covid")
def test_create_dataset(cleaner, capsys):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        return manage_dataset.create_dataset(PROJECT_ID)

    response = run_sample()
    cleaner.append(response.name)

    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out


@pytest.mark.skip(reason="service is limited due to covid")
def test_list_dataset(capsys, dataset):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        manage_dataset.list_datasets(PROJECT_ID)

    run_sample()
    out, _ = capsys.readouterr()
    assert dataset.name in out


@pytest.mark.skip(reason="service is limited due to covid")
def test_get_dataset(capsys, dataset):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        manage_dataset.get_dataset(dataset.name)

    run_sample()
    out, _ = capsys.readouterr()
    assert "The dataset resource name:" in out


@pytest.mark.skip(reason="service is limited due to covid")
def test_delete_dataset(capsys, dataset):
    @backoff.on_exception(
        backoff.expo, ServerError, max_time=testing_lib.RETRY_DEADLINE
    )
    def run_sample():
        manage_dataset.delete_dataset(dataset.name)

    run_sample()
    out, _ = capsys.readouterr()
    assert "Dataset deleted." in out
