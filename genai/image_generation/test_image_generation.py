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

import imggen_canny_ctrl_type_with_txt_img
import imggen_mmflash_edit_img_with_txt_img
import imggen_mmflash_txt_and_img_with_txt
import imggen_mmflash_with_txt
import imggen_raw_reference_with_txt_img
import imggen_scribble_ctrl_type_with_txt_img
import imggen_style_reference_with_txt_img
import imggen_subj_refer_ctrl_refer_with_txt_imgs
import imggen_with_txt


os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# The project name is included in the CICD pipeline
# os.environ['GOOGLE_CLOUD_PROJECT'] = "add-your-project-name"

GCS_OUTPUT_BUCKET = "python-docs-samples-tests"
RESOURCES = os.path.join(os.path.dirname(__file__), "test_resources")
OUTPUT_FILE = os.path.join(RESOURCES, "dog_newspaper.png")


@pytest.fixture(scope="session")
def output_gcs_uri() -> str:
    prefix = f"text_output/{dt.now()}"

    yield f"gs://{GCS_OUTPUT_BUCKET}/{prefix}"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_OUTPUT_BUCKET)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        blob.delete()


def test_img_generation(output_gcs_uri: str) -> None:
    response = imggen_with_txt.generate_images(
        OUTPUT_FILE
    )
    assert response


def test_img_customization_subject(output_gcs_uri: str) -> None:
    response = imggen_subj_refer_ctrl_refer_with_txt_imgs.subject_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_img_customization_style(output_gcs_uri: str) -> None:
    response = imggen_style_reference_with_txt_img.style_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_img_customization_style_transfer(output_gcs_uri: str) -> None:
    response = imggen_raw_reference_with_txt_img.style_transfer_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_img_customization_scribble(output_gcs_uri: str) -> None:
    response = imggen_scribble_ctrl_type_with_txt_img.scribble_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_img_customization_canny_edge(output_gcs_uri: str) -> None:
    response = imggen_canny_ctrl_type_with_txt_img.canny_edge_customization(
        output_gcs_uri=output_gcs_uri
    )
    assert response


def test_imggen_mmflash_examples() -> None:
    # generate image
    fname = imggen_mmflash_with_txt.generate_content()
    assert os.path.isfile(fname)
    # edit generate image
    new_fname = imggen_mmflash_edit_img_with_txt_img.generate_content()
    assert os.path.isfile(new_fname)

    # clean-up
    os.remove(fname)
    os.remove(new_fname)


def test_imggen_mmflash_txt_and_img_with_txt() -> None:
    last_image_id = imggen_mmflash_txt_and_img_with_txt.generate_content()
    # clean-up
    for i in range(last_image_id + 1):
        img_name = f"example-image-{i+1}.png"
        if os.path.isfile(img_name):
            os.remove(img_name)
    fname = "paella-recipe.md"
    if os.path.isfile(fname):
        os.remove(fname)
