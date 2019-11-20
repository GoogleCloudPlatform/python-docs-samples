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

from google.cloud.automl_v1beta1.gapic import enums

import automl_tables_predict
import automl_tables_model
import model_test

PROJECT = os.environ["GCLOUD_PROJECT"]
REGION = "us-central1"
STATIC_MODEL = model_test.STATIC_MODEL


def test_predict(capsys):
    inputs = {
        "Age": 31,
        "Balance": 200,
        "Campaign": 2,
        "Contact": "cellular",
        "Day": 4,
        "Default": "no",
        "Duration": 12,
        "Education": "primary",
        "Housing": "yes",
        "Job": "blue-collar",
        "Loan": "no",
        "MaritalStatus": "divorced",
        "Month": "jul",
        "PDays": 4,
        "POutcome": '0',
        "Previous": 12,
    }

    ensure_model_online()
    automl_tables_predict.predict(PROJECT, REGION, STATIC_MODEL, inputs)
    out, _ = capsys.readouterr()
    assert 'Predicted class name:' in out
    assert 'Predicted class score:' in out


def ensure_model_online():
    model = model_test.ensure_model_ready()
    if model.deployment_state != enums.Model.DeploymentState.DEPLOYED:
        automl_tables_model.deploy_model(PROJECT, REGION, model.display_name)

    return automl_tables_model.get_model(PROJECT, REGION, model.display_name)
