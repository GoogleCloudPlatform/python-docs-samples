# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

import pytest

import data_processing_helper  # noqa: I100 - lint incorrectly wants to group this before pytest


OUTPUT_FILENAME = f"test-processed-data-{uuid.uuid4()}.csv"


@pytest.fixture(autouse=True)
def teardown():
    yield
    try:
        os.remove(OUTPUT_FILENAME)
    except FileNotFoundError:
        print("No file to delete")


def test_data_processing_helper():
    assert OUTPUT_FILENAME not in os.listdir()
    data_processing_helper.preprocess_station_data(
        "ghcnd-stations.txt", OUTPUT_FILENAME
    )
    assert OUTPUT_FILENAME in os.listdir()
