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

import automl_translation_model

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
compute_region = "us-central1"


def test_model_list_get_evaluate(capsys):
    # list models
    automl_translation_model.list_models(project_id, compute_region, "")
    out, _ = capsys.readouterr()
    list_models_output = out.splitlines()
    assert "Model id: " in list_models_output[2]

    # get model
    model_id = list_models_output[2].split()[2]
    automl_translation_model.get_model(project_id, compute_region, model_id)
    out, _ = capsys.readouterr()
    assert "Model name: " in out
