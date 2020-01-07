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

import deploy_model

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
MODEL_ID = "TRL0000000000000000000"


@pytest.mark.slow
def test_deploy_model(capsys):
    # As model deployment can take a long time, instead try to deploy a
    # nonexistent model and confirm that the model was not found, but other
    # elements of the request were valid.
    try:
        deploy_model.deploy_model(PROJECT_ID, MODEL_ID)
        out, _ = capsys.readouterr()
        assert "The model does not exist" in out
    except Exception as e:
        assert "The model does not exist" in e.message
