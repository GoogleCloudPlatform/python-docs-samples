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

from google.cloud import automl
import pytest

import vision_classification_predict

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
MODEL_ID = os.environ["VISION_CLASSIFICATION_MODEL_ID"]


@pytest.fixture(scope="function", autouse=True)
def setup():
    # Verify the model is deployed before tyring to predict
    client = automl.AutoMlClient()
    model_full_id = client.model_path(PROJECT_ID, "us-central1", MODEL_ID)

    model = client.get_model(name=model_full_id)
    if model.deployment_state == automl.Model.DeploymentState.UNDEPLOYED:
        # Deploy model if it is not deployed
        response = client.deploy_model(name=model_full_id)
        response.result()


def test_vision_classification_predict(capsys):
    file_path = "resources/test.png"
    vision_classification_predict.predict(PROJECT_ID, MODEL_ID, file_path)
    out, _ = capsys.readouterr()
    assert "Predicted class name:" in out
