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

import pytest

import automl_vision_object_detection_deploy_model
import automl_vision_object_detection_deploy_node_count
import automl_vision_object_detection_undeploy_model

PROJECT_ID = os.environ['GCLOUD_PROJECT']
MODEL_ID = 'IOD6143103405779845120'


@pytest.mark.slow
def test_object_detection_deploy_undeploy_model(capsys):
    automl_vision_object_detection_deploy_model.deploy_model(
        PROJECT_ID, MODEL_ID)

    out, _ = capsys.readouterr()
    assert 'Model deployment finished' in out

    automl_vision_object_detection_undeploy_model.undeploy_model(
        PROJECT_ID, MODEL_ID)

    out, _ = capsys.readouterr()
    assert 'Model undeploy finished' in out


@pytest.mark.slow
def test_object_detection_deploy_node_count_undeploy_model(capsys):
    automl_vision_object_detection_deploy_node_count.deploy_model_node_count(
        PROJECT_ID, MODEL_ID)

    out, _ = capsys.readouterr()
    assert 'Model deployment on 2 nodes finished' in out

    automl_vision_object_detection_undeploy_model.undeploy_model(
        PROJECT_ID, MODEL_ID)

    out, _ = capsys.readouterr()
    assert 'Model undeploy finished' in out
