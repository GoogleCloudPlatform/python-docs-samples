#!/usr/bin/env python

# Copyright 2020 Google LLC
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

from google.cloud.automl_v1beta1 import Model

import pytest

import automl_tables_model
import automl_tables_predict
import model_test


PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
REGION = "us-central1"
STATIC_MODEL = model_test.STATIC_MODEL
GCS_INPUT = f"gs://{PROJECT}-automl-tables-test/bank-marketing.csv"
GCS_OUTPUT = f"gs://{PROJECT}-automl-tables-test/TABLE_TEST_OUTPUT/"
BQ_INPUT = f"bq://{PROJECT}.automl_test.bank_marketing"
BQ_OUTPUT = f"bq://{PROJECT}"
PARAMS = {}


@pytest.mark.slow
def test_batch_predict(capsys):
    ensure_model_online()

    automl_tables_predict.batch_predict(
        PROJECT, REGION, STATIC_MODEL, GCS_INPUT, GCS_OUTPUT, PARAMS
    )
    out, _ = capsys.readouterr()
    assert "Batch prediction complete" in out


@pytest.mark.slow
def test_batch_predict_bq(capsys):
    ensure_model_online()
    automl_tables_predict.batch_predict_bq(
        PROJECT, REGION, STATIC_MODEL, BQ_INPUT, BQ_OUTPUT, PARAMS
    )
    out, _ = capsys.readouterr()
    assert "Batch prediction complete" in out


def ensure_model_online():
    model = model_test.ensure_model_ready()
    if model.deployment_state != Model.DeploymentState.DEPLOYED:
        automl_tables_model.deploy_model(PROJECT, REGION, model.display_name)

    return automl_tables_model.get_model(PROJECT, REGION, model.display_name)
