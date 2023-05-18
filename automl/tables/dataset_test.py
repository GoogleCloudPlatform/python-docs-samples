#!/usr/bin/env python

# Copyright 2019 Google LLC
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
import random
import string
import time

from google.api_core import exceptions
import pytest

import automl_tables_dataset


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
STATIC_DATASET = "do_not_delete_this_table_python"
GCS_DATASET = ("gs://python-docs-samples-tests-automl-tables-test"
               "/bank-marketing.csv")

ID = "{rand}_{time}".format(
    rand="".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(4)]
    ),
    time=int(time.time()),
)


def _id(name):
    return f"{name}_{ID}"


def ensure_dataset_ready():
    dataset = None
    name = STATIC_DATASET
    try:
        dataset = automl_tables_dataset.get_dataset(PROJECT, REGION, name)
    except exceptions.NotFound:
        dataset = automl_tables_dataset.create_dataset(PROJECT, REGION, name)

    if dataset.example_count is None or dataset.example_count == 0:
        automl_tables_dataset.import_data(PROJECT, REGION, name, GCS_DATASET)
        dataset = automl_tables_dataset.get_dataset(PROJECT, REGION, name)

    automl_tables_dataset.update_dataset(
        PROJECT,
        REGION,
        dataset.display_name,
        target_column_spec_name="Deposit",
    )

    return dataset


@pytest.mark.slow
def test_dataset_create_import_delete(capsys):
    name = _id("d_cr_dl")
    dataset = automl_tables_dataset.create_dataset(PROJECT, REGION, name)
    assert dataset is not None
    assert dataset.display_name == name

    automl_tables_dataset.import_data(PROJECT, REGION, name, GCS_DATASET)

    out, _ = capsys.readouterr()
    assert "Data imported." in out

    automl_tables_dataset.delete_dataset(PROJECT, REGION, name)

    with pytest.raises(exceptions.NotFound):
        automl_tables_dataset.get_dataset(PROJECT, REGION, name)


def test_dataset_update(capsys):
    dataset = ensure_dataset_ready()
    automl_tables_dataset.update_dataset(
        PROJECT,
        REGION,
        dataset.display_name,
        target_column_spec_name="Deposit",
        weight_column_spec_name="Balance",
    )

    out, _ = capsys.readouterr()
    assert "Target column updated." in out
    assert "Weight column updated." in out


def test_list_datasets():
    ensure_dataset_ready()
    assert (
        next(
            (
                d
                for d in automl_tables_dataset.list_datasets(PROJECT, REGION)
                if d.display_name == STATIC_DATASET
            ),
            None,
        )
        is not None
    )
