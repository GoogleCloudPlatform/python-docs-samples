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

import os

from google.cloud import aiplatform

import list_tuned_models



_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
_LOCATION = "us-central1"


def test_list_tuned_models():
    tuned_model_names = list_tuned_models.list_tuned_models(
        _PROJECT_ID,
        _LOCATION,
    )
    filtered_models_counter = 0
    for tuned_model_name in tuned_model_names:
        model_registry = aiplatform.models.ModelRegistry(model=tuned_model_name)
        if (
            'Vertex LLM Test Fixture '
            '(list_tuned_models_test.py::test_list_tuned_models)'
        ) in model_registry.get_version_info('1').model_display_name:
            filtered_models_counter += 1
    assert filtered_models_counter == 1
