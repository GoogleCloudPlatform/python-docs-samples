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

from datetime import datetime as dt

import os

from google.cloud import storage

import pytest

import videogen_with_img

import videogen_with_txt


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"

GCS_OUTPUT_BUCKET = "python-docs-samples-tests"


@pytest.fixture(scope="session")
def output_gcs_uri() -> str:
    prefix = f"text_output/{dt.now()}"

    yield f"gs://{GCS_OUTPUT_BUCKET}/{prefix}"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        blob.delete()


def test_videogen_with_txt(output_gcs_uri: str) -> None:
    response = videogen_with_txt.generate_videos(output_gcs_uri=output_gcs_uri)
    assert response


def test_videogen_with_img(output_gcs_uri: str) -> None:
    response = videogen_with_img.generate_videos_from_image(output_gcs_uri=output_gcs_uri)
    assert response
