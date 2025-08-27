# Copyright 2021 Google LLC
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

import datetime
import os
import random
from typing import Generator

from google.cloud import bigquery

import pytest


@pytest.fixture(scope="session")
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture(scope="session")
def dataset(project_id: str) -> Generator[bigquery.Dataset, None, None]:
    client = bigquery.Client()

    # Add a random suffix to dataset name to avoid conflict, because we run
    # a samples test on each supported Python version almost at the same time.
    dataset_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    suffix = f"_{(random.randint(0, 99)):02d}"
    dataset_name = "samples_tests_" + dataset_time + suffix

    dataset_id = "{}.{}".format(project_id, dataset_name)
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "us-east7"
    created_dataset = client.create_dataset(dataset)
    yield created_dataset

    client.delete_dataset(created_dataset, delete_contents=True)
