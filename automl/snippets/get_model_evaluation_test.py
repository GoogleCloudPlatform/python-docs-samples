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

from google.cloud import automl
import pytest

import get_model_evaluation

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
MODEL_ID = os.environ["ENTITY_EXTRACTION_MODEL_ID"]


@pytest.fixture(scope="function")
def model_evaluation_id():
    client = automl.AutoMlClient()
    model_full_id = client.model_path(PROJECT_ID, "us-central1", MODEL_ID)
    evaluation = None
    for e in client.list_model_evaluations(parent=model_full_id, filter=""):
        evaluation = e
        break
    model_evaluation_id = evaluation.name.split(
        "{}/modelEvaluations/".format(MODEL_ID)
    )[1].split("\n")[0]
    yield model_evaluation_id


def test_get_model_evaluation(capsys, model_evaluation_id):
    get_model_evaluation.get_model_evaluation(PROJECT_ID, MODEL_ID, model_evaluation_id)
    out, _ = capsys.readouterr()
    assert "Model evaluation name: " in out
