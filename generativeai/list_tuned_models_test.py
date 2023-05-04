# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from vertex_ai.preview.language_models import TextGenerationModel, TextEmbeddingModel

import list_tuned_models

_PROJECT_ID = "YOUR_PROJECT_ID"
_LOCATION = "us-central1"


def test_list_tuned_models():
    tuned_model_names = list_tuned_models.list_tuned_models(_PROJECT_ID, _LOCATION)
    assert len(tuned_model_names) > 0
    for tuned_model_name in tuned_model_names:
      assert tuned_model_name.startswith('projects/_PROJECT_ID/locations/us-central1/models/')
