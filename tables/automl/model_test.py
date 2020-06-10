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

import automl_tables_model
import dataset_test


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
STATIC_MODEL = "do_not_delete_this_model_0"
GCS_DATASET = "gs://cloud-ml-tables-data/bank-marketing.csv"

ID = "{rand}_{time}".format(
    rand="".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(4)]
    ),
    time=int(time.time()),
)


def _id(name):
    return "{}_{}".format(name, ID)


def test_list_models():
    ensure_model_ready()
    assert (
        next(
            (
                m
                for m in automl_tables_model.list_models(PROJECT, REGION)
                if m.display_name == STATIC_MODEL
            ),
            None,
        )
        is not None
    )


def test_list_model_evaluations():
    model = ensure_model_ready()
    mes = automl_tables_model.list_model_evaluations(
        PROJECT, REGION, model.display_name
    )
    assert len(mes) > 0
    for me in mes:
        assert me.name.startswith(model.name)


def test_get_model_evaluations():
    model = ensure_model_ready()
    me = automl_tables_model.list_model_evaluations(
        PROJECT, REGION, model.display_name
    )[0]
    mep = automl_tables_model.get_model_evaluation(
        PROJECT,
        REGION,
        model.name.rpartition("/")[2],
        me.name.rpartition("/")[2],
    )

    assert mep.name == me.name


def ensure_model_ready():
    name = STATIC_MODEL
    try:
        return automl_tables_model.get_model(PROJECT, REGION, name)
    except exceptions.NotFound:
        pass

    dataset = dataset_test.ensure_dataset_ready()
    return automl_tables_model.create_model(
        PROJECT, REGION, dataset.display_name, name, 1000
    )
