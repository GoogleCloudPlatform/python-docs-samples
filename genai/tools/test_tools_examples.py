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

import tools_code_exec_with_txt
import tools_code_exec_with_txt_local_img
import tools_func_def_with_txt
import tools_func_desc_with_txt
import tools_google_search_with_txt
import tools_vais_with_txt

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_tools_code_exec_with_txt() -> None:
    response = tools_code_exec_with_txt.generate_content()
    assert response


def test_tools_code_exec_with_txt_local_img() -> None:
    response = tools_code_exec_with_txt_local_img.generate_content()
    assert response


def test_tools_func_def_with_txt() -> None:
    response = tools_func_def_with_txt.generate_content()
    assert response


def test_tools_func_desc_with_txt() -> None:
    response = tools_func_desc_with_txt.generate_content()
    assert response


def test_tools_google_search_with_txt() -> None:
    response = tools_google_search_with_txt.generate_content()
    assert response


def test_tools_vais_with_txt() -> None:
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    datastore = f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/grounding-test-datastore"
    response = tools_vais_with_txt.generate_content(datastore)
    assert response
