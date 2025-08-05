# Copyright 2025 Google LLC
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

#
# Using Google Cloud Vertex AI to test the code samples.
#

import os

import ctrlgen_with_class_schema
import ctrlgen_with_enum_class_schema
import ctrlgen_with_enum_schema
import ctrlgen_with_nested_class_schema
import ctrlgen_with_nullable_schema
import ctrlgen_with_resp_schema

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"  # "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_ctrlgen_with_class_schema() -> None:
    assert ctrlgen_with_class_schema.generate_content()


def test_ctrlgen_with_enum_class_schema() -> None:
    assert ctrlgen_with_enum_class_schema.generate_content()


def test_ctrlgen_with_enum_schema() -> None:
    assert ctrlgen_with_enum_schema.generate_content()


def test_ctrlgen_with_nested_class_schema() -> None:
    assert ctrlgen_with_nested_class_schema.generate_content()


def test_ctrlgen_with_nullable_schema() -> None:
    assert ctrlgen_with_nullable_schema.generate_content()


def test_ctrlgen_with_resp_schema() -> None:
    assert ctrlgen_with_resp_schema.generate_content()
