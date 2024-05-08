# Copyright 2024 Google LLC
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

import multimodal_embedding_advanced
import multimodal_embedding_basic

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
location = "us-central1"
MODEL_ID = "multimodalembedding@001"


def test_multimodal_embedding_basic() -> None:
    response = multimodal_embedding_basic.generate_content(
        PROJECT_ID, location, MODEL_ID)
    assert response


def test_multimodal_embedding_advanced() -> None:
    response = multimodal_embedding_advanced.generate_content(
        PROJECT_ID, location, MODEL_ID)
    assert response
