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

import code_retrieval_example
import embeddings_docretrieval_with_txt
import model_tuning_example
import multimodal_example

os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"


def test_embeddings_docretrieval_with_txt() -> None:
    response = embeddings_docretrieval_with_txt.embed_content()
    assert response


def test_code_retrieval_example() -> None:
    response = code_retrieval_example.embed_test()
    assert response


def test_model_tuning_example() -> None:
    response = model_tuning_example.tune_embedding_model()
    assert response


def test_multimodal_example() -> None:
    response = multimodal_example.get_image_video_text_embeddings()
    assert response
