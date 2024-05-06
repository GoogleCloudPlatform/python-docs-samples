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

import grounding_private_data_basic
import grounding_public_data_basic


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = "us-central1"
MODEL_ID = "gemini-1.5-pro-preview-0409"
DATASTORE = ""


def test_grounding_public_data_basic() -> None:
    response = grounding_public_data_basic.generate_content(PROJECT_ID, REGION, MODEL_ID)
    assert response


def test_grounding_private_data_basic() -> None:
    response = grounding_private_data_basic.generate_content(
        PROJECT_ID, REGION, MODEL_ID, DATASTORE
    )
    assert response
