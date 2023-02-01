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

import get_model

PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
MODEL_ID = os.environ["ENTITY_EXTRACTION_MODEL_ID"]


def test_get_model(capsys):
    get_model.get_model(PROJECT_ID, MODEL_ID)
    out, _ = capsys.readouterr()
    assert "Model id: " in out
