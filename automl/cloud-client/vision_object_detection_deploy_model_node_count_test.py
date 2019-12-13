#!/usr/bin/env python

# Copyright 2018 Google LLC
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
import sys

import pytest

import vision_object_detection_deploy_model_node_count

PROJECT_ID = os.environ["GCLOUD_PROJECT"]

version_info = sys.version_info
if version_info.major == 3 and version_info.minor == 6:
    MODEL_ID = "IOD1729298694026559488"
else:
    MODEL_ID = "IOD6143103405779845120"


@pytest.fixture(scope="function")
def verify_model_state():
    from google.cloud import automl

    client = automl.AutoMlClient()
    model_full_id = client.model_path(PROJECT_ID, "us-central1", MODEL_ID)

    model = client.get_model(model_full_id)
    if model.deployment_state == automl.enums.Model.DeploymentState.DEPLOYED:
        # Undeploy model if it is deployed
        response = client.undeploy_model(model_full_id)
        response.result()


@pytest.mark.slow
def test_vision_object_detection_deploy_model(capsys, verify_model_state):
    verify_model_state
    vision_object_detection_deploy_model_node_count.deploy_model_with_node_count(
        PROJECT_ID, MODEL_ID
    )
    out, _ = capsys.readouterr()
    assert "Model deployment finished." in out
