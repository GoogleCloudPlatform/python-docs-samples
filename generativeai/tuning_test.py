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

from google.cloud.aiplatform.private_preview.language_models import TextEmbeddingModel

import tuning

_TRAINING_DATASET = "gs://..."
_PROJECT_ID = "YOUR_PROJECT_ID"
_LOCATION = "us-south1"


def test_tuning():
    content = tuning.tuning(_TRAINING_DATASET, _PROJECT_ID, _LOCATION)
    assert "VR" in content
